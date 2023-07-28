from random import randint
from rest_framework import generics, status, permissions, response, views
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, UserSerializer
from .models import User
from rest_framework.views import APIView


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        username = self.request.data['username']
        email = self.request.data['email']
        password = self.request.data['password']
        if User.objects.filter(username=username, is_active=True).first():
            return response.Response({'message': "This number already exist"}, status=status.HTTP_302_FOUND)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return response.Response({"success": True, 'message': "User created please login!!!"},
                                 status=status.HTTP_200_OK)


class LoginAPI(generics.GenericAPIView):
    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            return response.Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        token = Token.objects.get_or_create(user=user)
        data = {
            'message': 'User logged',
            'token': str(token),
            'user_id': user.id
        }
        return response.Response({"success": True, 'data': data},
                                 status=status.HTTP_200_OK)


class ChangePasswordAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        user = request.user
        pas1 = request.data['password']
        pas2 = request.data['old_password']
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(pas2):
            user.set_password(pas1)
            user.save()
            return response.Response({'success': True, 'message': 'Successfully changed password'})
        return response.Response({'message': 'old password incorrect'}, status=400)


class UserRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(instance=self.request.user, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
