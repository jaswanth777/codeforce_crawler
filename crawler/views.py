from django.shortcuts import render,redirect,HttpResponse
import bs4
import requests
from .forms import HandleForm
import datetime
import json
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
def submission_stats(request,handle):
    URL = 'https://codeforces.com/api/user.status?handle='+handle
    data = requests.get(URL).json()
    ok = 0
    compilation_error = 0
    runtime_error = 0
    wrong_answer = 0
    time_limit_exceed = 0
    hacked = 0
    others = 0
    datemap = {}
    for rows in data['result']:
        date =  datetime.datetime.fromtimestamp(rows['creationTimeSeconds']).date().strftime('%Y-%m-%d')
        print(date)
        if date in datemap.keys():
            datemap[date] += 1
        else:
            datemap[date] = 1
        if rows.get('verdict') is not None:
            verdict = rows['verdict']
            if verdict == "OK":
                ok += 1
            elif verdict == "COMPILATION_ERROR":
                compilation_error += 1
            elif verdict == "RUNTIME_ERROR":
                runtime_error += 1
            elif verdict == "WRONG_ANSWER":
                wrong_answer += 1
            elif verdict == "TIME_LIMIT_EXCEEDED":
                time_limit_exceed += 1
            elif verdict == "HACKED":
                hacked += 1
            else:
                others += 1
    datemapjson = json.dumps(datemap)



    context = {
        'handle': handle,
        'ok': ok,
        'compilation_error': compilation_error,
        'runtime_error': runtime_error,
        'wrong_answer': wrong_answer,
        'time_limit_exceed': time_limit_exceed,
        'hacked' : hacked,
        'others' : others,
        'heatmap' : datemapjson
    }
    return render(request, "crawler/submission_stats.html", context)