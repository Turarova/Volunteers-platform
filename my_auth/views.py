from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.generics import ListAPIView, GenericAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from .helpers import send_confirmation_email

# from rest_framework.views import APIView


User = get_user_model()

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_confirmation_email(user, user.activation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"msg":"You successfully logged out"}, status=status.HTTP_204_NO_CONTENT)


class ActivationView(GenericAPIView):
    serializer_class = ActivationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data['activation_code']
            user = get_object_or_404(User, activation_code=code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg':'User successfully activated'})


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )



class DeleteUserView(DestroyAPIView):
    serializer_class = DeleteUserSerializer
    permission_classes = (IsAdminUser,)

    @swagger_auto_schema(request_body=DeleteUserSerializer)
    def delete(self, request):
        serializers = self.serializer_class(data=request.data)
        if serializers.is_valid(raise_exception=True):
            email = serializers.validated_data['email']
            user = get_object_or_404(User, email=email)
            self.perform_destroy(user)
            return Response({"msg":"User is successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
            