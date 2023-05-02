import os
from django.urls import path, include
from django.conf import settings
from . import views

# We have to execute a piece of code once. as urls.py is imported once only so we can place out code block here
if not os.path.exists(settings.FILE_PATH_DIRECTORY):
    #  TODO: might run with root privs
    os.mkdir(settings.FILE_PATH_DIRECTORY)  # this might get an error due to OS permission
    print(f"Created Storage Directory: {settings.FILE_PATH_DIRECTORY}")

urlpatterns = [
    path("", views.home, name="storage_home"),
    path("login/", views.login_user, name="storage_login"),
    path("dashboard/", views.list_directories, name="storage_dashboard"),
    path("dashboard/<path:dir_path>/", views.list_directories, name="storage_dir_path"),
    path("logout/", views.logout_user, name="storage_logout"),
    path("signup/", views.SignUpView.as_view(), name="storage_signup"),
]
