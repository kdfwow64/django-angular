"""User authentication module."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from ..models.auth import User
from ..forms.auth import RegistrationForm, LoginForm
# Create your views here.


def signin(request):
    """User sign in."""
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            data = form.data.dict()
            user = authenticate(request, email=data.get(
                'email'), password=data.get('password'))
            # Review if statement.  I dont think it is getting here before
            # error
            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome %s %s.' %
                                 (user.email, user.full_name))
                return redirect('dashboard')
            else:
                messages.success(request, 'Invalid credentials')
                return redirect('auth_signin')
        else:
            messages.success(request, 'Invalid credentials')
            return redirect('auth_signin')
    else:
        form = LoginForm()

    # load sign in template
    return render(request, 'auth/signin.html', {'form': form, 'title': 'Sign In'})


def signout(request):
    logout(request)
    return redirect('auth_signin')


def register(request):
    """
    Handle requests to the /register route.

    Add an User to the database through the registration form
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            data = form.data.dict()
            del(data['csrfmiddlewaretoken'])
            del(data['confirm_password'])
            user = User.objects.create_user(**data)
            user.is_active = False
            user.save()
    else:
        form = RegistrationForm()

    # load registration template
    return render(request, 'auth/register.html', {'form': form, 'title': 'Register'})
