from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Portfolio
from .serializers import SiteSerializer


class SiteDetailView(generics.RetrieveAPIView):
    """
    Public: fetch a live portfolio's rendered HTML/CSS by subdomain.
    Powers wildcard-serve ({subdomain}.forge.app). 404 unless live.
    """
    serializer_class = SiteSerializer
    permission_classes = [AllowAny]
    authentication_classes = []
    lookup_field = "subdomain"

    def get_queryset(self):
        return Portfolio.objects.filter(deployment_status="live")
