from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from utils.pagination import CustomPagination
from utils.permission import IsManagerOrDispatcher
from utils.CustomResponse import CustomResponse
from .filters import DriverFilter
from .models import DeleveryRunStatus, DeliveryRun, Driver
from .serializers import *
from .services import delivery_run_service


class DriverListView(ListAPIView):
    queryset = Driver.objects.all().order_by('-created_at')
    serializer_class = DriverSerializer
    permission_classes = [IsManagerOrDispatcher]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = DriverFilter
    search_fields = ['name', 'phone']


class DeliveryRunListView(ListAPIView):
    queryset = DeliveryRun.objects.all().select_related('driver').order_by('-start_date')
    serializer_class = DeliveryRunSerializer
    permission_classes = [IsManagerOrDispatcher]
    pagination_class = CustomPagination


class BuildDeliveryRunView(APIView):
    permission_classes = [IsManagerOrDispatcher]

    def post(self, request, *args, **kwargs):
        serializer = BuildDeliveryRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            run = delivery_run_service.build_run(serializer.validated_data['driver_id'])
        except Exception as exc:
            return CustomResponse.error(
                message='Driver is not available',
                error={'driver_id': str(exc)},
                status=400,)

        return CustomResponse.success(
            message='Delivery run built',
            data=DeliveryRunSerializer(run).data,
            status=201,)


class DeliveryRunStartView(APIView):
    permission_classes = [IsManagerOrDispatcher]

    def post(self, request, *args, **kwargs):
        delivery_run = DeliveryRun.objects.get(pk=kwargs['pk'])
        if delivery_run.status != DeleveryRunStatus.ASSIGNED:
            return CustomResponse.error(
                message='Delivery run is not in assigned status',
                status=400,)

        delivery_run.status = DeleveryRunStatus.EN_ROUTE
        delivery_run.save()
        return CustomResponse.success(
            message='Delivery run en route',
            data=DeliveryRunSerializer(delivery_run).data,
            status=200,)