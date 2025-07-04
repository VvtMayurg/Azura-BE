from rest_framework.response import Response
from rest_framework.views import View


class HomeView(View):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "active",
                "version": "1",
                "releaseId": "1.0.0",
                "description": "Health of DigiMedix service",
                "links": {"API Docs": "/api/docs/"},
            },
        )
