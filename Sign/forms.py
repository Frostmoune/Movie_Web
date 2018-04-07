from django import forms

# 登录信息模块
class SigninForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)

# 注册信息模块
class SignupForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50)