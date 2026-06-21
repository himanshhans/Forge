from django.db.models import F
from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.portfolios.models import Portfolio
from apps.portfolios.niches import list_niches
from .models import ShowcaseEntry
from .serializers import ShowcaseEntrySerializer

SORTS = {
    "newest": "-created_at",
    "oldest": "created_at",
    "most_viewed": "-view_count",
}


class ShowcaseListView(generics.ListAPIView):
    """Public gallery off the showcase_index view. Filter by niche, sort, search."""
    serializer_class = ShowcaseEntrySerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_queryset(self):
        qs = ShowcaseEntry.objects.all()
        niche = self.request.query_params.get("niche")
        if niche:
            qs = qs.filter(niche=niche)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search)
        sort = SORTS.get(self.request.query_params.get("sort", "newest"), "-created_at")
        return qs.order_by(sort)

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)
        # Attach niche facets for filter UI.
        resp.data = {
            "portfolios": resp.data,
            "niches": [
                {"id": n["niche_id"], "name": n["display_name"]}
                for n in list_niches()
            ],
        }
        return resp


class ShowcaseDetailView(generics.RetrieveAPIView):
    serializer_class = ShowcaseEntrySerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = "portfolio_id"

    def get_queryset(self):
        return ShowcaseEntry.objects.all()


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def increment_view(request, portfolio_id):
    """Increment a portfolio's view count (atomic). Public."""
    updated = Portfolio.objects.filter(id=portfolio_id).update(views=F("views") + 1)
    if not updated:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    p = Portfolio.objects.get(id=portfolio_id)
    return Response({"view_count": p.views})
