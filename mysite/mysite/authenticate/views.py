from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm
# Create your views here.


def home(request):
    return render(request, 'authenticate/home.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('Loged in with {}'.format(username)))
            return redirect('home')
        messages.success(request, ('error'))
        return redirect('login')
    return render(request, 'authenticate/login.html')


def logout_user(request):
    logout(request)
    messages.success(request, ('logged out'))
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Register")
            return redirect('home')

    form = SignUpForm(request.POST)
    context = {'form': form}
    return render(request, 'authenticate/register.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated")
            return redirect('home')

    form = EditProfileForm(request.POST, instance=request.user)
    context = {'form': form}
    return render(request, 'authenticate/edit_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            # update session to prevent user from logging out user after password update
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed")
            return redirect('home')

    form = PasswordChangeForm(data=request.POST, user=request.user)
    context = {'form': form}
    return render(request, 'authenticate/change_password.html', context)
