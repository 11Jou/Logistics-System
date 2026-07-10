from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from utils.pagination import CustomPagination
from utils.permission import IsManagerOrDispatcher

from .filters import OrderFilter
from .models import Order
from .serializers import OrderSerializer


class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsManagerOrDispatcher]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = OrderFilter
    search_fields = ['customer_name', 'customer_phone', 'address']