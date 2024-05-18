from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_and_register(request):
    return render(request, 'login_and_register.html')

# login view
def user_login(request):
    if request.method == 'POST':
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # print(email, password, request is None)
        # user = authenticate(request, username=username, password=password)
        
        if(len(password) < 8):
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères')
            return  render(request, 'login_and_register.html', {'showLogin':True, 'email': email})
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)    # we can use alogin which is a asynvhrone method for login a user
            return redirect('home')
        else:
            print('Out')
            messages.error(request, 'Email ou mot de passe incorrect')
            return render(request, 'login_and_register.html', {'showLogin':True, 'email': email})
    else: 
        return redirect('login_and_register')

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        
        print(username, email, password, confirm_password)

        data = { 'username': username, 'email': email }
        if(len(password) < 8):
            messages.error(request, 'Le mot de passe doit contenir au moins 8 caractères')
            return  render(request, 'login_and_register.html', {'stay': True, 'showRegister':True, 'data': data})
        if(password != confirm_password):
            messages.error(request, 'Les mots de passe ne correspondent pas')
            return  render(request, 'login_and_register.html', {'stay': True, 'showRegister':True, 'data': data})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save() # save the user
        return redirect('login_and_register')
    else:
        return redirect('login_and_register')

def user_logout(request):
    logout(request)
    return redirect('login_and_register')