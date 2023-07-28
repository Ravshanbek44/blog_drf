from django.urls import path
from .views import LoginAPI, RegisterAPI, ChangePasswordAPI, UserRUDAPIView

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('user-rud/', UserRUDAPIView.as_view()),
    path('change-password/', ChangePasswordAPI.as_view())
]
