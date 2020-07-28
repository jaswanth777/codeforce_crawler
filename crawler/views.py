from django.shortcuts import render,redirect,HttpResponse
import bs4
import requests
from .forms import HandleForm
# Create your views here.

def home(request):
    if request.method=='POST':
        form=HandleForm(request.POST)
        if form.is_valid():
            handle=form.cleaned_data.get('handle')
            return redirect('/display/'+handle)
    else:
            form=HandleForm()

    return render(request,'crawler/home.html',{'form':form})

def display(request,handle):
    context={
        'handle':handle,
    }
    return render(request,'crawler/display.html',context)
