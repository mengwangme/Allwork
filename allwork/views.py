from django.shortcuts import render

def home(request):
    """
    Renders home template
    """
    return render(request, 'home.html')