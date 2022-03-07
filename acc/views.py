from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'acc/index.html')

def login_user(request):
    if request.method == 'POST':
        un = request.POST.get('uname')
        pw = request.POST.get('upass')
        user = authenticate(username = un, password = pw)
        if user:
            login(request, user)
            messages.success(request, f'{user}님 환영합니다.')
            return redirect('acc:index')
        else:
            messages.error(request, "계정정보가 일치하지 않습니다.")
    return render(request, 'acc/login.html')

def logout_user(request):
    logout(request)
    return redirect('acc:login')

def signup(request):
    if request.method == 'POST':
        un = request.POST.get('uname')
        up = request.POST.get('upass')
        ua = request.POST.get('uage')
        uc = request.POST.get('ucom')
        ui = request.FILES.get('upic')
        try:
            User.objects.create_user(username = un, password = up, age = ua, comment = uc, pic = ui)
        except:
            messages.error(request, "USERNAME이 이미 존재합니다.")
        return redirect('acc:login')
    return render(request, 'acc/signup.html')

def profile(request):
    return render(request, 'acc/profile.html')

def delete(request):
    ck = request.POST.get('ckpw')
    if check_password(ck, request.user.password): # check_password(평문, 비문) 비교해서 맞으면 True
        request.user.pic.delete()
        request.user.delete()
        return redirect('acc:index')
    else:
        messages.error(request, "계정정보가 일치하지 않습니다.")
    return redirect('acc:profile')

def update(request):
    if request.method == 'POST':
        u = request.user
        un = request.POST.get('uname')
        up = request.POST.get('upass')
        ua = request.POST.get('uage')
        uc = request.POST.get('ucom')
        ui = request.FILES.get('upic')
        
        u.username = un
        if up:
            User.set_password(up)
        u.age = ua
        u.comment = uc
        if ui:
            u.pic.delete()
            u.pic = ui
        u.save()
        login(request, u)
        return redirect('acc:profile')
    return render(request, 'acc/update.html')

