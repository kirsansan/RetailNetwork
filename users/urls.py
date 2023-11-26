from django.urls import path
from rest_framework import routers

from users.apps import UsersConfig
from users.views import UserViewSet, MyTokenObtainPairView

from rest_framework_simplejwt.views import (TokenRefreshView)

app_name = UsersConfig.name

urlpatterns = [
    # work with tokens
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = routers.SimpleRouter()
router.register('', UserViewSet)

urlpatterns += router.urls
