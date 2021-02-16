from __future__ import unicode_literals
from django.http import JsonResponse
from django.shortcuts import render


def index(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'sign_up.html')


def health(request):
    state = {"status": "UP"}
    return JsonResponse(state)


def handler404(request):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)
