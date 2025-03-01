from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *

urlpatterns = [
    path('create-company/', CompanyCreateView.as_view(), name='create_company'),
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('register-user/', CompleteRegistrationView.as_view(), name='register_user'),
    path('activation/', ActivationView.as_view()),
    path('delete-user/', DeleteUserAPIView.as_view(), name='delete_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/request/', PasswordResetRequestAPIView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),

]





















# # from rest_framework_simplejwt.views import TokenRefreshView

# # from . import views

# # urlpatterns = [
# #     path('register/', views.RegisterView.as_view()),
# #     path('login/', views.LoginView.as_view()),
# #     path('activation/', views.ActivationView.as_view()),
# #     path('users/', views.UserListAPIView.as_view()),
# #     path('logout/', views.LogoutAPIView.as_view()),
# #     path('delete/', views.DeleteUserView.as_view()),
# #     path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
# # ]