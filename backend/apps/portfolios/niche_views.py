from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .niches import get_niche, list_niches


class NicheListView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = None

    def get(self, _request):
        return Response({"niches": list_niches()})


class NicheDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, _request, niche_id):
        niche = get_niche(niche_id)
        if not niche:
            return Response({"error": "Unknown niche"}, status=404)
        return Response(niche)
