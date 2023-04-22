from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.conf import settings
from .forms import SignUpForm
from .models import StorageUser
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
            dir_name = dir_obj.dir_uuid.urn[9:]
            path = settings.FILE_PATH_DIRECTORY / dir_name

            # check if directory exists
            if not os.path.exists(path):
                os.mkdir(path)

        return response


def home(request: HttpRequest):
    return render(request, "storage/storage-home.html")


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


# def create_user_storage_profile(request: HttpRequest):


def dashboard(request: HttpRequest):
    return render(request, "storage/storage-dashboard.html")
