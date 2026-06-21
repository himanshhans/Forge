from django.urls import path

from .views import ShowcaseDetailView, ShowcaseListView, increment_view

urlpatterns = [
    path("", ShowcaseListView.as_view(), name="gallery-list"),
    path("<uuid:portfolio_id>/", ShowcaseDetailView.as_view(), name="gallery-detail"),
    path("<uuid:portfolio_id>/view/", increment_view, name="gallery-view"),
]
