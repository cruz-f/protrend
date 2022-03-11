from django.shortcuts import render


def best_practices(request):
    return render(request, 'api/best-practices.html')
