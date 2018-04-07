from django import forms

class SigninForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)

class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)