from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from utils.pagination import CustomPagination
from utils.permission import IsManagerOrDispatcher
from utils.CustomResponse import CustomResponse

from .filters import DriverFilter
from .repository.delivery_run_repository import DeliveryRunRepository
from .repository.driver_repository import DriverRepository
from .serializers import (
    BuildDeliveryRunSerializer,
    DeliveryRunSerializer,
    DriverSerializer,
)
from .services.delivery_run_service import DeliveryRunService


class DriverListView(ListAPIView):
    queryset = DriverRepository.get_all_ordered()
    serializer_class = DriverSerializer
    permission_classes = [IsManagerOrDispatcher]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = DriverFilter
    search_fields = ['name', 'phone']


class DeliveryRunListView(ListAPIView):
    queryset = DeliveryRunRepository.get_all_with_driver()
    serializer_class = DeliveryRunSerializer
    permission_classes = [IsManagerOrDispatcher]
    pagination_class = CustomPagination


class BuildDeliveryRunView(APIView):
    permission_classes = [IsManagerOrDispatcher]

    def post(self, request, *args, **kwargs):
        serializer = BuildDeliveryRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            run = DeliveryRunService.build_run(serializer.validated_data['driver_id'])
        except Exception as exc:
            return CustomResponse.error(
                message='Driver is not available',
                error={'driver_id': str(exc)},
                status=400,
            )

        return CustomResponse.success(
            message='Delivery run built',
            data=DeliveryRunSerializer(run).data,
            status=201,
        )
