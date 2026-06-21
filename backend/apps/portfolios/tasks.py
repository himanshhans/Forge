"""
Async generation pipeline (Celery). In dev (no Redis) these run eager/inline.

Flow:
  generate_portfolio_task
    -> LLM text  (status: text_pending -> text_done)
    -> if avatar needs server gen: generate_avatar_task (avatar_pending -> avatar_done)
       else: avatar_done immediately
    -> publish   (publishing -> live)
"""
import logging

from celery import shared_task

from services.avatar_service import AvatarError, generate_avatar
from services.llm_service import LLMError
from services.portfolio_generator import generate_portfolio
from services.publisher import publish_portfolio
from .models import AvatarGeneration, Portfolio

logger = logging.getLogger(__name__)

SERVER_GEN_AVATARS = {"2d_illustrated", "ai_photo"}


@shared_task
def generate_portfolio_task(portfolio_id):
    try:
        p = Portfolio.objects.get(id=portfolio_id)
    except Portfolio.DoesNotExist:
        logger.error("Portfolio %s missing", portfolio_id)
        return

    # 1. LLM text
    try:
        result, provider = generate_portfolio(
            p.niche, p.questionnaire, p.intro_card, p.avatar_url
        )
    except LLMError as e:
        logger.error("Generation failed for %s: %s", portfolio_id, e)
        p.generation_status = "failed"
        p.save(update_fields=["generation_status"])
        return

    p.generated_html = result["html"]
    p.generated_css = result["css"]
    p.generated_metadata = result["metadata"]
    p.llm_provider = provider
    p.generation_status = "text_done"
    p.save(update_fields=[
        "generated_html", "generated_css", "generated_metadata",
        "llm_provider", "generation_status",
    ])

    # 2. Avatar (only if server-side gen needed)
    if p.avatar_type in SERVER_GEN_AVATARS and not p.avatar_url:
        p.generation_status = "avatar_pending"
        p.save(update_fields=["generation_status"])
        generate_avatar_task(str(p.id))  # inline-safe; eager in dev
        p.refresh_from_db()
        if p.generation_status == "failed":
            return  # avatar failed; text preserved, don't publish yet
    else:
        p.generation_status = "avatar_done"
        p.save(update_fields=["generation_status"])

    # 3. Publish
    p.generation_status = "publishing"
    p.save(update_fields=["generation_status"])
    publish_portfolio(p)


@shared_task
def generate_avatar_task(portfolio_id):
    try:
        p = Portfolio.objects.get(id=portfolio_id)
    except Portfolio.DoesNotExist:
        return

    description = (p.avatar_generation_data or {}).get("description", "")
    gen = AvatarGeneration(portfolio=p, avatar_type=p.avatar_type)
    try:
        out = generate_avatar(p.avatar_type, description)
    except AvatarError as e:
        logger.error("Avatar gen failed for %s: %s", portfolio_id, e)
        gen.provider = "replicate"
        gen.success = False
        gen.error_message = str(e)
        gen.save()
        p.generation_status = "failed"
        p.save(update_fields=["generation_status"])
        return

    gen.provider = out["provider"]
    gen.provider_id = out.get("provider_id", "")
    gen.prompt = description
    gen.generated_url = out["url"]
    gen.cost_cents = out.get("cost_cents")
    gen.generation_time_ms = out.get("generation_time_ms")
    gen.success = True
    gen.save()

    p.avatar_url = out["url"]
    p.generation_status = "avatar_done"
    p.save(update_fields=["avatar_url", "generation_status"])
