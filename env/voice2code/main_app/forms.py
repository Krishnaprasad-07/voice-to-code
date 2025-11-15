from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
   
    class Meta:
        model = Register
        fields = ['first_name', 'last_name','username', 'email', 'password', 'contact']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder':'User Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}),
            'contact': forms.TextInput(attrs={'class': 'form-control','placeholder':'Contact'}),
        }
        help_texts = {
            'username': None,
        }
        labels={
            'first_name':'',
            'last_name':'',
            'username':'',
            'email':'',
            'password':'',
            'contact':'',
        }
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label=''
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Password'}), label='')
    
class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'email', 'contact']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}),
            'contact': forms.TextInput(attrs={'class': 'form-control','placeholder':'Contact'}),
        }
        help_texts = {
            'username': None,
        }
        labels={
            'first_name':'',
            'last_name':'',
            'email':'',
            'contact':'',
        }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Old Password'}),label='')
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'New Password'}),label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}),label='' )    

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'Email'}),label='')
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'New Password'}),label='')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirm Password'}),label='')
    