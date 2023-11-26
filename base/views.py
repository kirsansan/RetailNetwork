from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from base.models import NetworkNode, Counterparty, Product
from base.paginators import AllListsPaginator
from base.permissions import IsActive, IsAdministrator
from base.serializers import NetworkNodeSerializer, NetworkNodeCreationSerializer, CounterpartySerializer, \
    ProductSerializer


class NodesPublicAPIView(ListAPIView):
    """Nodes list-view """
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]
    pagination_class = AllListsPaginator

    # def get_queryset(self):
    #     """ only active user have permission for view all nodes"""
    #     user = self.request.user
    #     if user.is_superuser or user.groups.filter(name='moderator').exists():
    #         return Habit.objects.all()
    #     else:
    #         print("You are not allowed to public")
    #         return Habit.objects.filter(is_public=True)


class NodesDetailAPIView(RetrieveAPIView):
    """Node detail view"""
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]


class NodesDeleteAPIView(DestroyAPIView):
    """Node delete"""
    queryset = NetworkNode.objects.all()
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]


class NodesCreateAPIView(CreateAPIView):
    """Node create"""
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeCreationSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]

    # def perform_create(self, serializer):
    #     """save owner(creator) of Habit"""
    #     new_habit = serializer.save()
    #     new_habit.creator = self.request.user
    #     new_habit.save()
    #     new_log = SenderDailyLog(habit_id=new_habit, daily_status=SenderDailyLog.CREATE)
    #     new_log.save()


class NodesUpdateAPIView(UpdateAPIView):
    """Node update"""
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]


class CounterpartyViewSet(ModelViewSet):
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



