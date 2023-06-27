from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import SignUpForm
from .models import StorageUser
from . import utils
import os


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    template_name = "storage/storage-signup.html"
    success_url = reverse_lazy("storage_home")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/dashboard")
        return super(SignUpView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(SignUpView, self).form_valid(form)

        username = form.cleaned_data['username']
        user = User.objects.get(username=username)

        if user:
            storage_user = StorageUser.objects.create(username=user)
            storage_user.save()

        dir_obj = StorageUser.objects.get(username=user)
        if dir_obj:
            dir_name = utils.get_uuid_as_string(dir_obj.dir_uuid)
            path = settings.FILE_PATH_DIRECTORY / dir_name

            # check if directory exists
            if not os.path.exists(path):
                os.mkdir(path)

        return response


def login_user(request: HttpRequest):
    # if user is already authenticated
    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/dashboard")

        return render(request, "storage/storage-login.html", context={
            "message": "Invalid username or password"
        })

    return render(request, "storage/storage-login.html")


def logout_user(request: HttpRequest):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


def home(request: HttpRequest):
    # if the user is already logged in redirect to dashboard
    if request.user.is_authenticated:
        return redirect("/dashboard")

    return render(request, "storage/storage-home.html")


@login_required(login_url="/login/")
def dashboard(request: HttpRequest, dir_path: str = ""):
    username = request.user.username
    storage_result = utils.get_current_user_storage_path(username)
    user_storage_path = storage_result.get("user_storage_path")

    if user_storage_path:
        blob_detail = utils.find_valid_path(user_storage_path, dir_path)
        if blob_detail.get("is_redirect_required"):
            # if the user has entered a wrong file path url then it will be routed to the correct optimal url
            return redirect(f"/dashboard/{blob_detail.get('redirect_path')}")

        current_dir_files = blob_detail.get("files")
        backtracking_paths = utils.find_url(f"dashboard/{dir_path}")

        return render(request, "storage/storage-dashboard.html", context={
            "paths": backtracking_paths,
            "files": current_dir_files
        })

    return redirect("/error")


def upload_files(request: HttpRequest):
    """
    uploads files to theirs respective account owner's directories
    """


def error(request: HttpRequest):
    """
    shows an error page to the user
    """
    return render(request, "storage/storage-error.html")
