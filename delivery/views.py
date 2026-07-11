from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from utils.pagination import CustomPagination
from utils.permission import IsManagerOrDispatcher, IsDriver
from utils.CustomResponse import CustomResponse
from .filters import DriverFilter
from .models import DeleveryRunStatus, DeliveryRun, Driver
from .serializers import *
from .services import delivery_run_service, delivery_stop_service


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

    @swagger_auto_schema(request_body=BuildDeliveryRunSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BuildDeliveryRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            run = delivery_run_service.build_run(serializer.validated_data['driver_id'])
        except Exception as exc:
            return CustomResponse.error(
                message=str(exc),
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
        if delivery_run.status != DeleveryRunStatus.ASSIGNED or delivery_run.status == DeleveryRunStatus.EN_ROUTE:
            return CustomResponse.error(
                message='Delivery run is not in assigned or en route status',
                status=400,)

        delivery_run.status = DeleveryRunStatus.EN_ROUTE
        delivery_run.save()
        return CustomResponse.success(
            message='Delivery run en route',
            data=DeliveryRunSerializer(delivery_run).data,
            status=200,)


class DeliveryRunCashBankedView(APIView):
    permission_classes = [IsManagerOrDispatcher]

    def put(self, request, *args, **kwargs):
        try:
            run = delivery_run_service.cash_banked_run(run_id=kwargs['pk'])
        except Exception as exc:
            return CustomResponse.error(
                message=str(exc),
                error={'detail': str(exc)},
                status=400,
            )
        return CustomResponse.success(
            message='Delivery run cash banked',
            data=DeliveryRunSerializer(run).data,
            status=200,
        )

class DriverDeliveryRunListView(ListAPIView):
    queryset = DeliveryRun.objects.all().select_related('driver').order_by('-start_date')
    serializer_class = DeliveryRunSerializer
    permission_classes = [IsDriver]
    pagination_class = CustomPagination

    def get_queryset(self):
        current_driver = Driver.objects.get(user=self.request.user)
        return self.queryset.filter(driver=current_driver)


class DriverDeliveryRunDetailView(RetrieveAPIView):
    queryset = DeliveryRun.objects.all().select_related('driver').order_by('-start_date')
    serializer_class = DeliveryRunSerializer
    permission_classes = [IsDriver]

    def retrieve(self, request, *args, **kwargs):
        current_driver = Driver.objects.get(user=self.request.user)
        try:
            delivery_run = self.queryset.get(driver=current_driver, id=kwargs['pk'])
        except DeliveryRun.DoesNotExist:
            return CustomResponse.error(
                message='Delivery run not found',
                error={'detail': 'Delivery run does not exist or does not belong to this driver'},
                status=404,
            )

        return CustomResponse.success(
            message='Delivery run retrieved',
            data=self.get_serializer(delivery_run).data,
            status=200,
        )


class DriverDeliveryStopStartView(APIView):
    permission_classes = [IsDriver]
    serializer_class = DeliveryStopSerializer

    def put(self, request, *args, **kwargs):
        try:
            stop = delivery_stop_service.start_stop(
                user=request.user,
                run_id=kwargs['pk'],
                stop_id=kwargs['stop_pk'],
            )
        except Exception as exc:
            return CustomResponse.error(
                message=str(exc),
                error={'detail': str(exc)},
                status=400,
            )

        return CustomResponse.success(
            message='Delivery stop started',
            data=DeliveryStopSerializer(stop).data,
            status=200,
        )


class DriverDeliveryStopDeliveredView(APIView):
    permission_classes = [IsDriver]
    serializer_class = DeliveryStopSerializer


    def put(self, request, *args, **kwargs):
        try:
            stop = delivery_stop_service.deliver_stop(
                user=request.user,
                run_id=kwargs['pk'],
                stop_id=kwargs['stop_pk'],
            )
        except Exception as exc:
            return CustomResponse.error(
                message=str(exc),
                error={'detail': str(exc)},
                status=400,
            )

        return CustomResponse.success(
            message='Delivery stop delivered',
            data=DeliveryStopSerializer(stop).data,
            status=200,
        )

class DriverDeliveryStopFailedView(APIView):
    permission_classes = [IsDriver]

    @swagger_auto_schema(request_body=FailDeliveryStopSerializer)
    def put(self, request, *args, **kwargs):
        serializer = FailDeliveryStopSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            stop = delivery_stop_service.fail_stop(
                user=request.user,
                run_id=kwargs['pk'],
                stop_id=kwargs['stop_pk'],
                failed_reason=serializer.validated_data['failed_reason'],
            )
        except Exception as exc:
            return CustomResponse.error(
                message=str(exc),
                error={'detail': str(exc)},
                status=400,
            )

        return CustomResponse.success(
            message='Delivery stop failed',
            data=DeliveryStopSerializer(stop).data,
            status=200,
        )

class DriverDeliveryRunCompleteView(APIView):
    permission_classes = [IsDriver]

    def put(self, request, *args, **kwargs):
        try:
            run = delivery_run_service.complete_run(
                user=request.user,
                run_id=kwargs['pk'],
            )
        except Exception as exc:
            return CustomResponse.error(
                message=str(exc),
                error={'detail': str(exc)},
                status=400,
            )

        return CustomResponse.success(
            message='Delivery run completed',
            data=DeliveryRunSerializer(run).data,
            status=200,
        )