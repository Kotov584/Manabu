from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('token', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('books/<int:id>', BookView().as_view(), name = 'booksby'),
    path('books', BookView().as_view(), name = 'books'),
    path('', BookView().as_view(), name = 'home'),
    path('hello', HelloView().as_view(), name = 'hi')
]