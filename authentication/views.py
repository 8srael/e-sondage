from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.contrib.auth.models import User


# Create your views here.

def login_and_register(request):
    return render(request, 'login_and_register.html')

# login view
def login(request):
    if request.method == 'POST':    
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)    
            return HttpResponse('Logged in')
        return render(request, 'login_and_register.html', {'login_error': 'Nom d\'utilisateur ou mot de passe incorrect'})
    else: 
        return render(request, 'login_and_register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        
        print(username, email, password, confirm_password)

        if(len(password) < 8):
            return render(request, 'login_and_register.html', {'register_error': 'Le mot de passe doit contenir au moins 8 caractères', 'stay' : True})
        if(password != confirm_password):
            return render(request, 'login_and_register.html', {'register_error': 'Les mots de passe ne correspondent pas', 'stay' : True})

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save() # save the user
        return redirect('login_and_register')
    else:
        return render(request, 'login_and_register.html')