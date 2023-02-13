from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 
from rest_framework import permissions
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group, Permission
from permissions import *
from app.models import Book 
from generic import GenericAPIView

class BookView(GenericAPIView):
    model_class = Book
    permission_classes = [IsAuthenticated, ReadDataPermission] 

    def get(self, request, *args, **kwargs): 
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class HelloView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Please provide an email'}, status=status.HTTP_400_BAD_REQUEST)

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        token = urlsafe_base64_encode(force_bytes(user.pk)).decode()

        send_mail(
            'Password Reset',
            'Please follow this link to reset your password: http://localhost:8000/reset_password/{}'.format(token),
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return Response({'success': 'An email has been sent with the password reset link'}, status=status.HTTP_200_OK)

class RegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)

class ResetPasswordView(APIView):
    def post(self, request, token):
        UserModel = get_user_model()

        try:
            user_id = force_text(urlsafe_base64_decode(token))
            user = UserModel.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None

        if user is None:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

        password = request.data.get('password')
        newPassword = request.data.get('new_password')
        newPasswordAgain = request.data.get('new_password_again')

        if not password:
            return Response({'error': 'Please provide a password'}, status=status.HTTP_400_BAD_REQUEST)

        if newPassword != newPasswordAgain:
            return Response({'error': 'Please double check your new password is the same'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(newPassword)
        user.save()
        update_session_auth_hash(request, user)
        return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)