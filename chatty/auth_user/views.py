from auth_user.serializers import UserSerializer, CustomObtainTokenSerializer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class UserCreateView(generics.CreateAPIView):
    """
    A view that allows creating a user with the provided data.
    It uses the 'UserSerializer' serializer to serialize and deserialize the user data.
    It has the 'AllowAny' permission class, which means it can be accessed by anyone, even unauthenticated users.
    """
    permission_classes = (
        AllowAny,
    )
    serializer_class = UserSerializer


class UserLoginView(TokenObtainPairView):
    """
    A view that authenticates a user with the provided email
    and password and returns a JWT access and refresh token pair.
    It uses the 'CustomObtainTokenSerializer' serializer to customize the token response.
    It has the 'AllowAny' permission class,
    which means it can be accessed by anyone, even unauthenticated users.
    """
    permission_classes = (
        AllowAny,
    )
    serializer_class = CustomObtainTokenSerializer


class UserLogoutView(APIView):
    """
    A view that allows revoking a refresh token, thus logging out the user.
    It has the 'IsAuthenticated' permission class,
    which means it can only be accessed by authenticated users.
    It expects a 'refresh' token in the request data
    and blacklists it using the 'RefreshToken' class from 'rest_framework_simplejwt'.
    It returns a 'Successful Logout' message on success and a '400 Bad Request' on failure.
    """
    permission_classes = (
        IsAuthenticated,
    )

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist()
            return Response('Successful Logout', status=status.HTTP_205_RESET_CONTENT)
        except Exception as exc:
            return Response(status=status.HTTP_400_BAD_REQUEST)
