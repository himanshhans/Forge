from rest_framework.routers import DefaultRouter

from .niche_views import NicheDetailView, NicheListView
from .site_views import SiteByDomainView, SiteDetailView
from .views import PortfolioViewSet
from django.urls import path

router = DefaultRouter()
router.register(r"portfolios", PortfolioViewSet, basename="portfolio")

urlpatterns = [
    path("niches/", NicheListView.as_view(), name="niche-list"),
    path("niches/<str:niche_id>/", NicheDetailView.as_view(), name="niche-detail"),
    path("sites/by-domain/", SiteByDomainView.as_view(), name="site-by-domain"),
    path("sites/<str:subdomain>/", SiteDetailView.as_view(), name="site-detail"),
]
urlpatterns += router.urls
