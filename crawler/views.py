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
def contest_stats(request,handle):
    contests=[]
    ranks=[]
    rating=[]
    c_url="https://codeforces.com/api/user.rating?handle="+handle
    res=requests.get(c_url)
    data=res.json()
    for val in data['result']:
        contests.append(val['contestId'])
        ranks.append(val['rank'])

        rating.append(val['newRating'])
    context={
        'handle':handle,
        'contests':contests,
        'ranks':ranks,
        'rating':rating
    }
    return render(request,'crawler/contest_stats.html',context)
