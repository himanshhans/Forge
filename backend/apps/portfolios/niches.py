"""
Hardcoded niche configs (5 stable niches). No DB table.
Source of truth for questionnaire fields, generation prompt key, showcase sort,
default CTAs, SEO schema. Frontend pulls via GET /api/v1/niches/.
"""

NICHES = {
    "indie_hacker": {
        "niche_id": "indie_hacker",
        "display_name": "Indie Hacker",
        "description": "Showcase products you shipped, revenue, and metrics",
        "icon": "rocket",
        "color": "#3b82f6",
        "questionnaire_fields": [
            "name", "headline", "projects", "revenue", "users",
            "github", "producthunt", "tech_stack", "looking_for",
        ],
        "generation_prompt": "indie_hacker",
        "showcase_metrics": ["revenue", "users", "projects_shipped"],
        "default_ctas": ["Let's build together", "Hire me as co-founder"],
        "seo_schema": "Person+Portfolio",
    },
    "freelancer": {
        "niche_id": "freelancer",
        "display_name": "Freelancer",
        "description": "Portfolio, case studies, rates, testimonials, booking",
        "icon": "briefcase",
        "color": "#10b981",
        "questionnaire_fields": [
            "name", "services", "past_work", "rates",
            "testimonials", "booking_link", "availability",
        ],
        "generation_prompt": "freelancer",
        "showcase_metrics": ["service_category", "rating", "reviews"],
        "default_ctas": ["Hire me", "Book a call", "View rates"],
        "seo_schema": "Person+Portfolio",
    },
    "creator": {
        "niche_id": "creator",
        "display_name": "Creator",
        "description": "Social stats, video embeds, sponsorship/support links",
        "icon": "video",
        "color": "#ef4444",
        "questionnaire_fields": [
            "name", "content_type", "channels", "subscriber_counts",
            "popular_content", "patreon_kofi",
        ],
        "generation_prompt": "creator",
        "showcase_metrics": ["followers", "engagement_rate", "video_count"],
        "default_ctas": ["Subscribe", "Join Patreon", "Follow me"],
        "seo_schema": "Person+Portfolio",
    },
    "coach": {
        "niche_id": "coach",
        "display_name": "Coach/Consultant",
        "description": "Services, credentials, testimonials, booking",
        "icon": "academic-cap",
        "color": "#8b5cf6",
        "questionnaire_fields": [
            "name", "expertise", "credentials", "services",
            "testimonials", "pricing", "calendly_link",
        ],
        "generation_prompt": "coach",
        "showcase_metrics": ["specialty", "rating", "testimonial_count"],
        "default_ctas": ["Book a call", "Schedule 1:1", "Get started"],
        "seo_schema": "Person+Portfolio",
    },
    "agency": {
        "niche_id": "agency",
        "display_name": "Agency",
        "description": "Team showcase, case studies, services, client list",
        "icon": "building-office",
        "color": "#f59e0b",
        "questionnaire_fields": [
            "company_name", "tagline", "services", "team_members",
            "case_studies", "tech_stack", "contact",
        ],
        "generation_prompt": "agency",
        "showcase_metrics": ["specialization", "team_size", "client_count"],
        "default_ctas": ["Get a quote", "Start project", "Schedule consultation"],
        "seo_schema": "LocalBusiness+Organization",
    },
}


def get_niche(niche_id: str) -> dict | None:
    return NICHES.get(niche_id)


def list_niches() -> list[dict]:
    return list(NICHES.values())
