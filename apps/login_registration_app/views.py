from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import re, bcrypt

# Create your views here.
def login_registration(request):
    print("Log in and registration")
    if 'logged_user' not in request.session:
        print("Not logged in")
        return render(request, 'login_registration.html')
    else:
        print("Already logged in")
        return render(request, 'login_registration.html')

def register(request):
    print("Register")
    if request.method == 'POST':
        form = request.POST
        errors = User.objects.validate_registration(form)
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            if User.objects.register(form):
                messages.success(request, "You have successfully created an account")
            else:
                messages.error(request, "Something went wrong")
    return redirect('/login_registration')

def login(request):
    print("Log in")
    if request.method != 'POST':
        return redirect('/login_registration')
    user = User.objects.login(request.POST)
    if user:
        request.session['logged_user'] = user.id
        return redirect('/login_registration')
    else:
        messages.error(request, "Invalid login")
        return redirect('/login_registration')
