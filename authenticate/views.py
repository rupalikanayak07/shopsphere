from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from base.models import *

# Create your views here.
def login_(request):
    if request.method== 'POST':
        username= request.POST['username']
        password= request.POST['password']
        u= authenticate(username=username,password=password)
        if u:
            login(request,u)
            return redirect('home')
        else:
            return render(request,'login_.html',{'status':True,'login_nav':True})


    return render(request,'login_.html',{'login_nav':True})

def register(request):

    if request.method== 'POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        email= request.POST['email']
        username= request.POST['username']
        password= request.POST['password']

        a=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        a.set_password(password)
        a.save()


    return render(request,'register.html',{'login_nav':True})

def profile(request):
    cartproducts_count=cartmodel.objects.filter(host=request.user).count()


    return render(request,'profile.html',{'profile_nav':True,'cartproducts_count':cartproducts_count})

def logout_(request):
    logout(request)
    return redirect('login_')


def update(request,pk):
    cartproducts_count=cartmodel.objects.filter(host=request.user).count()
    data= User.objects.get(id=pk)
    if request.method=='POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        email= request.POST['email']
        
        data.first_name=first_name
        data.last_name=last_name
        data.email=email
        data.save()
        return redirect('profile')
        
    return render(request,'update.html',{'data':data,'profile_nav':True,'cartproducts_count':cartproducts_count})


def reset_pass(request):
    cartproducts_count=cartmodel.objects.filter(host=request.user).count()
    user=request.user
    if request.method== 'POST':
        if 'oldpass' in request.POST:
            oldpass= request.POST['oldpass']
            auth_user=authenticate(username=user.username,password=oldpass)
            if auth_user:
                return render(request,'reset_pass.html',{'newpass':True})
            else:
                return render(request,'reset_pass.html',{'wrong':True})
            
        if 'newpass' in request.POST:
            newpass = request.POST['newpass']
            user.set_password(newpass)
            user.save()
            return redirect ('profile')

    return render(request,'reset_pass.html',{'profile_nav':True,'cartproducts_count':cartproducts_count})


def forget_pass(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        try:
            u=User.objects.get(username=username)
            request.session['fp_user']=u.username
            
            return redirect('newpass')
        except User.DoesNotExist:
            return render(request,'forget_pass.html',{'error':True,'login_nav':True})

    return render(request,'forget_pass.html',{'login_nav':True})

def newpass(request):
    username= request.session.get('fp_user')

    if username is None:
        return redirect('forget_pass')
    user=User.objects.get(username=username)

    
    if request.method=='POST':
        newpass= request.POST.get('password')

        if user.check_password(newpass):
            return render(request,'newpass.html',{'error':'new password should not same to old password','login_nav':True})
        
        user.set_password(newpass)
        user.save()

        del request.session['fp_user']
        return redirect('login_')

    return render(request,'newpass.html',{'login_nav':True})