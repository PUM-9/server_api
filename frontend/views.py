from django.shortcuts import render


def index(request):
    print("index")
    return render(request, 'frontend/index.html')
