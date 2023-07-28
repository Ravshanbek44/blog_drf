from django.urls import path
from . import views

urlpatterns = [
    path('blog-list/', views.BlogListAPIView.as_view()),
    path('blog/<int:pk>/', views.BlogGetByIdAPIView.as_view()),
    path('blog-update/<int:pk>/', views.BlogUpdateAPIView.as_view()),
    path('blog-delete/<int:pk>/', views.BlogDestroyAPIView.as_view()),
    path('blog-create/', views.BlogCreateAPIView.as_view()),

]
