from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import os
from . import models
from .menu_process import process
import requests
import datetime
import json
from json2html import *
from collections import defaultdict
from collections import Counter

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'login.html')
        
    elif request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')

def home(request):
    return render(request,'home.html')

@login_required
def dashboard(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request,'staff_dashboard.html')
    else:
        fi=open('static/menu/menu.json')
        menu=eval(fi.read())
        if menu:
            for date,date_menu in menu.items():
                menu[date]=json2html.convert(date_menu)
            context={'menu':menu}
            return render(request,'student_dashboard.html',context)
        else:
            return render(request,'student_dashboard.html')
        

@login_required
def menu_upload(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST' and request.FILES['upload']:
            upload = request.FILES['upload']
            try:
                os.remove('menu/'+str(upload.name))
            except:
                pass
            fss = FileSystemStorage(location='static/menu')
            file = fss.save(upload.name, upload)
            file_url = fss.url(file)
            result=process('static/menu'+requests.utils.unquote(file_url))
            models.MenuItem.objects.all().delete()
            models.Rating.objects.all().delete()
            for a,b in result.items():
                print(b)
                for c,d in b.items():
                    for k in d:
                        menuitem=models.MenuItem(date=a,name=k,meal_type=c)
                        menuitem.save()
            fi=open('static/menu/menu.json','w+')
            print(result,file=fi)
            fi.close()
            return render(request, 'menu_upload.html', {'uploaded': True})
        return render(request, 'menu_upload.html')
    else:
        return render(request,'student_dashboard.html')
    
@login_required
def file_complaint(request):
    if not request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST' and request.FILES['upload']:
            upload = request.FILES['upload']
            title=request.POST['title']
            description=request.POST['description']
            student=request.user.username
            date_time=datetime.datetime.now()
            fss = FileSystemStorage(location='static/complaints')
            file = fss.save(upload.name, upload)
            file_url = 'complaints'+requests.utils.unquote(fss.url(file))
            print(file_url)
            complaint=models.Complaint(date_time=date_time,student=student,file_url=file_url,title=title,description=description)
            complaint.save()
            return render(request, 'file_complaint.html', {'uploaded': True})
        return render(request, 'file_complaint.html')
    else:
        return render(request,'staff_dashboard.html')
    
@login_required
def view_complaints(request):
    if request.user.is_staff or request.user.is_superuser:
        data=models.Complaint.objects.all().values()
        context={'complaints':data}
        return render(request,'view_complaints.html',context)
    else:
        return render(request,'student_dashboard.html')

@login_required
def rate_menu(request):
    if not request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            item_id = request.POST['item_id']
            rating = request.POST['rating']
            ratings=models.Rating(user_id=request.user.username,item_id=item_id,rating=rating)
            ratings.save()
        menu=list(models.MenuItem.objects.all().values())
        your_ratings=list(models.Rating.objects.filter(user_id=request.user.username).values())
        print(menu)
        print(your_ratings)
        d = defaultdict(dict)
        for item in menu + your_ratings:
            d[item['item_id']].update(item)
        final=list(d.values())
        context={'menu':final}
        return render(request,'rate_menu.html',context)
    else:
        return render(request,'staff_dashboard.html')
@login_required
def view_ratings(request):
    if request.user.is_staff or request.user.is_superuser:
        item_ids=len(models.MenuItem.objects.all())
        print(item_ids)
        data=[]
        for i in range(1,item_ids+1):
            fetched=list(models.Rating.objects.filter(item_id=i).values())
            fetched2=list(models.MenuItem.objects.filter(item_id=i).values())[0]
            sum=0
            for j in fetched:
                sum+=j['rating']
            try:
                avg=sum/len(fetched)
            except:
                avg=0
            data.append({'item_id':i,'name':fetched2['name'],'date':fetched2['date'],'meal_type':fetched2['meal_type'],'avg_rating':avg})
        print(data)
        context={'data':data}
        return render(request,'view_ratings.html',context)
    else:
        return render(request,'student_dashboard.html')