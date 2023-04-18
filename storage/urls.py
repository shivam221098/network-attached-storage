from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="app_home"),
    path("login/", views.login_user, name="storage_login"),
    path("dashboard/", views.dashboard, name="storage_dashboard"),
    path("logout/", views.logout_user, name="storage_logout"),
]