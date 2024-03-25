from django.shortcuts import render

def Dashboard_View(request):
    return render(request, 'home.html')
