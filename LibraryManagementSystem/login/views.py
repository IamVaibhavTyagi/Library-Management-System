from pickle import NONE
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db import connection


def login_user(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('searchBook:index')
            # Redirect to a success page.
            ...
        else:
            # Return an 'invalid login' error message.
            print("inside error print")
            messages.success(
                request, ("Failed to login! Check your credentials and Try Again."))
            return redirect("login:login")
    else:
        return render(request, "login_page.html")


def logout_user(request):
    logout(request)
    print("inside logout print")
    messages.success(
        request, ("User logged out successfully!"))
    return redirect("login:login")


def register_user(request):
    print("inside registre user")
    form = UserCreationForm()
    if (request.method == 'POST'):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("inside form valid")
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('searchBook:index')

    return render(request, "signup_page.html", {'form': form})
    # if ('username' in request.POST) and ('password' in request.POST) and ('retypepassword' in request.POST):

    #     username = request.POST['username']
    #     password = request.POST['password']
    #     repassword = request.POST['retypepassword']
    #     if password == repassword:
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         return redirect('searchBook:index')
    #     else:
    #         messages.success(
    #             request, ("Passwords don't match!"))
    #         return redirect('login:signup')
    # else:
    #     messages.success(
    #         request, ("Fill the form correctly!"))
    #     return redirect('login:signup')
