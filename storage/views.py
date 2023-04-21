from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout
import os


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


def dashboard(request: HttpRequest):
    return render(request, "storage/storage-dashboard.html")
