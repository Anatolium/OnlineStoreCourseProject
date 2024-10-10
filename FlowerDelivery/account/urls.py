from django.urls import path, include
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout/', views.user_logout, name='logout'),
]
