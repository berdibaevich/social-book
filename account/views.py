from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Account
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from django.contrib import messages



# Create your views here.



# Register lika as Sign up Functions 
def register_view(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'Siz alleqashan dizimnen otkensiz yag\'niy {user.email}')
    page = 'signup'
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            account = authenticate(email = email, password = password)
            login(request, account)

            messages.success(request, 'Dizimnen awmetli ottin\'iz!')
            return redirect('myaccount:my-account', account.pk)


    context = {
        'form': form,
        'page': page
    }
    return render(request, 'account/register-form.html', context)

# / signup

# loginView
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            messages.info(request, 'Jane urinip korin\' mumkin email qaytedur yamasa password')
            return redirect('/')


    context = {
        'page': page
    }
    return render(request, 'account/register-form.html', context)


# /loginView


# logoutView

def logout_view(request):
    logout(request)
    return redirect('/')


# /





















