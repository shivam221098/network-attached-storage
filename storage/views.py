from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def home(request: HttpRequest):
    return HttpResponse("<a>Hello!<a>")
