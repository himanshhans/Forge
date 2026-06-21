from django.db import models


class ShowcaseEntry(models.Model):
    """
    Read-only model backed by the `showcase_index` SQL VIEW (not a table).
    View defined in migration 0001. No sync logic — always reflects portfolios.
    """
    portfolio_id = models.UUIDField(primary_key=True)
    user_id = models.UUIDField()
    username = models.CharField(max_length=150)
    title = models.CharField(max_length=255)
    niche = models.CharField(max_length=50)
    thumbnail_url = models.CharField(max_length=500)
    deployed_url = models.CharField(max_length=255)
    featured = models.BooleanField()
    featured_at = models.DateTimeField(null=True)
    view_count = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "showcase_index"
