from django.urls import path

from face.apps import FaceConfig
from face.views import home_page_view

app_name = FaceConfig.name

urlpatterns = [
    path('', home_page_view, name='index'),
]
