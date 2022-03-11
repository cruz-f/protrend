from django.shortcuts import render


def index(request):
    return render(request, "website/index.html", {'active_page': 'home'})


def fake_view(request, param=None):
    return render(request, "website/index.html", {'active_page': 'home'})
