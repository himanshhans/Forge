from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CardSiteView, CardVCardView, ContactCardViewSet

router = DefaultRouter()
router.register(r"cards", ContactCardViewSet, basename="card")

urlpatterns = [
    path("card-sites/<slug:slug>/", CardSiteView.as_view(), name="card-site"),
    path("card-sites/<slug:slug>/vcard/", CardVCardView.as_view(), name="card-vcard"),
]
urlpatterns += router.urls
