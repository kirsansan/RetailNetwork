from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from base.models import NetworkNode, Counterparty, Product
from base.paginators import AllListsPaginator
from base.permissions import IsActive, IsAdministrator
from base.serializers import NetworkNodeSerializer, NetworkNodeCreationSerializer, CounterpartySerializer, \
    ProductSerializer, NetworkNodeUpdateSerializer


class NodesPublicAPIView(ListAPIView):
    """Nodes list-view
    :param: country_filter = Country - you can use it as URL parameter for filtering"""
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]
    pagination_class = AllListsPaginator

    def get_queryset(self):
        """
        change the queryset with filter by country (if exist)
        only active user have permission for view all nodes"""
        custom_filter = self.request.query_params.get('country_filter')
        queryset = NetworkNode.objects.all()
        if custom_filter is not None:
            queryset = queryset.filter(contacts__country=custom_filter)
        return queryset


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


class NodesPlusCreateAPIView(CreateAPIView):
    """Node create with adding new address at the sme time"""
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]


class NodesUpdateAPIView(UpdateAPIView):
    """Node update"""
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeUpdateSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]


class CounterpartyViewSet(ModelViewSet):
    """CRUD for Contacts"""
    queryset = Counterparty.objects.all()
    serializer_class = CounterpartySerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]


class ProductViewSet(ModelViewSet):
    """CRUD for Products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsActive | IsAdministrator]
