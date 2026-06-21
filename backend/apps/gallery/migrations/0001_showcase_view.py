from django.db import migrations

CREATE_VIEW = """
CREATE VIEW showcase_index AS
SELECT
  p.id          AS portfolio_id,
  p.user_id     AS user_id,
  u.username    AS username,
  p.title       AS title,
  p.niche       AS niche,
  p.avatar_url  AS thumbnail_url,
  p.published_url AS deployed_url,
  p.is_featured AS featured,
  p.featured_at AS featured_at,
  p.views       AS view_count,
  p.created_at  AS created_at,
  p.updated_at  AS updated_at
FROM portfolios p
JOIN users u ON u.id = p.user_id
WHERE p.in_showcase = true
  AND p.deployment_status = 'live'
  AND u.is_public = true;
"""

DROP_VIEW = "DROP VIEW IF EXISTS showcase_index;"


class Migration(migrations.Migration):
    dependencies = [
        ("portfolios", "0002_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        # DROP first (idempotent), then CREATE. Each as its own statement
        # so sqlite (one stmt per execute) and Postgres both work.
        migrations.RunSQL(sql=[DROP_VIEW, CREATE_VIEW], reverse_sql=DROP_VIEW),
    ]
