from django.shortcuts import render

def initiate_view(request):
    return render(request, 'initiate/initiate.html')
