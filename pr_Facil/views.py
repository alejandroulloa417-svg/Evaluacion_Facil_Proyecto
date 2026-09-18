from django.shortcuts import render

def fn_index(request):
    return render(request, 'index.html')

def fn_index2(request):
    return render(request, 'index2.html')