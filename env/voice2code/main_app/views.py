from random import randint
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                data = Register.objects.get(username=username)
                request.session['uname'] = data.username
                request.session['ut'] = data.usertype
                request.session['uid'] = data.id
                messages.success(request, 'Login successful', extra_tags='alert alert-success')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password', extra_tags='alert alert-danger')
    else:
        form = LoginForm()  
    return render(request, 'signin.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.usertype = 'user'
            user.save()
            messages.success(request, 'Account created successfully', extra_tags='alert alert-success')
            return redirect('signin')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Logout successful', extra_tags='alert alert-success')
    return redirect('/')

@login_required
def profile(request):
    user_id = request.user.id
    user = Register.objects.get(id=user_id)
    return render(request, 'profile.html', {'user': user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully', extra_tags='alert alert-success')
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                if request.user.check_password(old_password):
                    request.user.set_password(new_password)
                    request.user.save()
                    messages.success(request, 'Password changed successfully', extra_tags='alert alert-success')
                    return redirect('profile')
                else:
                    messages.error(request, 'Invalid old password', extra_tags='alert alert-danger')
            else:
                messages.error(request, 'New password and confirm password does not match', extra_tags='alert alert-danger')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})




def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Register.objects.get(email=email)
                otp = randint(1000, 9999)
                user.otp = otp
                user.save()

                # Sending OTP via email
                subject = 'Your Password Reset OTP'
                message = f'Hello {user.username},\n\nYour OTP for password reset is: {otp}\n\nUse this OTP to reset your password. Do not share it with anyone.'
                from_email = settings.EMAIL_HOST_USER  # Replace with your email
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                messages.success(request, 'Password reset OTP sent to your email', extra_tags='alert alert-success')
                return redirect('signin')

            except Register.DoesNotExist:
                messages.error(request, 'Email not found. Please enter a registered email.', extra_tags='alert alert-danger')

    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            email = form.cleaned_data['email']
            if new_password == confirm_password:
                user = Register.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful', extra_tags='alert alert-success')
                return redirect('signin')
            else:
                messages.error(request, 'New password and confirm password does not match', extra_tags='alert alert-danger')
    else:  
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


@login_required
def view_users(request):
    users = Register.objects.filter(usertype="user")
    return render(request, 'view_users.html', {'users': users})


