from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ModelViewSet
from users.models import User

# from config.config import EMAIL_SENDING_SIMULATION_MODE
from users.permissions import IsOwner, IsAdmin
from users.serializers import UserSerializer, UserCreateSerializer, MyTokenObtainPairSerializer, \
    UserDetailSerializer, FullDetailSerializer


class UserViewSet(ModelViewSet):
    """all users procedures
       there you can
       - create
       - update
       - delete
       - get information (for all users list and extended information about yourself)
       """
    queryset = User.objects.all()
    default_serializer_class = UserSerializer
    serializers = {
        "create": UserCreateSerializer,
        "list": UserSerializer,
        "retrieve": UserDetailSerializer
    }
    default_permission = [AllowAny]
    permissions = {
        "create": [AllowAny],
        "update": [IsOwner],
        "partial_update": [IsOwner],
        "destroy": [IsAdmin],
        "retrieve": [IsAuthenticated],
        "list": [IsAuthenticated],
    }

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()

    def get_serializer_class(self):
        """ Return the serializer class
            if user want to see information about himself - let it be FullDetailSerializer"""
        # print("action=", self.action)
        # print("kwargs=", self.kwargs.get('pk'))
        # print("user", self.request.user.pk)
        i_wanna_be_serializer = self.serializers.get(self.action, self.default_serializer_class)
        if self.action == "retrieve":
            if not self.request.user.is_anonymous:
                if int(self.request.user.pk) == int(self.kwargs.get('pk')) or self.request.user.is_superuser:
                    i_wanna_be_serializer = FullDetailSerializer
        return i_wanna_be_serializer


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = MyTokenObtainPairSerializer
