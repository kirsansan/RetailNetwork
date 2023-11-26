from django.urls import path
from rest_framework import routers

from base.apps import BaseConfig
from base.views import NodesPublicAPIView, NodesCreateAPIView, NodesDeleteAPIView, NodesUpdateAPIView, \
    NodesDetailAPIView, CounterpartyViewSet, ProductViewSet, NodesPlusCreateAPIView

app_name = BaseConfig.name

urlpatterns = [
    # nodes

    path('all/', NodesPublicAPIView.as_view(), name='nodes listview'),
    # path('my/', NodesAPIView.as_view(), name='my nodes listview'),
    path('create/', NodesCreateAPIView.as_view(), name='create'),
    path('create_plus/', NodesPlusCreateAPIView.as_view(), name='create'),
    path('delete/<int:pk>/', NodesDeleteAPIView.as_view(), name='delete'),
    path('update/<int:pk>/', NodesUpdateAPIView.as_view(), name='update'),
    path('detail/<int:pk>/', NodesDetailAPIView.as_view(), name='detail'),

]

router1 = routers.SimpleRouter()
router1.register('contact', CounterpartyViewSet)
urlpatterns += router1.urls

router2 = routers.SimpleRouter()
router2.register('product', ProductViewSet)
urlpatterns += router2.urls
