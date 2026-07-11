from rest_framework.views import APIView

from utils.CustomResponse import CustomResponse
from utils.permission import IsManagerOrDispatcher

from .serializers import DashboardSerializer
from .services import get_dashboard_stats


class DashboardView(APIView):
    permission_classes = [IsManagerOrDispatcher]
    

    def get(self, request):
        serializer = DashboardSerializer(get_dashboard_stats())
        return CustomResponse.success(
            message='Dashboard stats retrieved',
            data=serializer.data,
            status=200,
        )
