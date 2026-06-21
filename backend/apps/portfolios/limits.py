"""Free-tier enforcement. Checked in service/view layer (not DB constraints)."""
from django.conf import settings
from rest_framework.exceptions import PermissionDenied

from .models import Portfolio


class PlanLimitExceeded(PermissionDenied):
    default_code = "plan_limit"


def check_can_create_portfolio(user):
    """Raise 403 if free-plan user already at portfolio cap."""
    if getattr(user, "is_pro", False):
        return
    count = Portfolio.objects.filter(user=user).count()
    if count >= settings.FREE_PLAN_MAX_PORTFOLIOS:
        raise PlanLimitExceeded(
            f"Free plan limit reached ({settings.FREE_PLAN_MAX_PORTFOLIOS} portfolio). "
            "Upgrade to Pro."
        )


def check_can_create_intro_card(user):
    """Free plan = 1 intro card. Intro card lives on a portfolio, so this mirrors
    the portfolio cap; kept separate for clarity / future divergence."""
    if getattr(user, "is_pro", False):
        return
    count = Portfolio.objects.filter(user=user).exclude(intro_card={}).count()
    if count >= settings.FREE_PLAN_MAX_INTRO_CARDS:
        raise PlanLimitExceeded(
            f"Free plan limit reached ({settings.FREE_PLAN_MAX_INTRO_CARDS} contact card). "
            "Upgrade to Pro."
        )
