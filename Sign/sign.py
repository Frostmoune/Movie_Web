from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt ,csrf_protect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .forms import SignupForm,SigninForm
from .views import index
from Movies import movie
from Movies.models import Movie,UserMovie
from Movies import movie as signmovie
import random
import os
import re

# 从ajax中获取注册信息
def getSignUp(request):
    infomation = {'isLogin':False,'userExist':False}
    if request.method=='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            # 判断用户是否存在
            user = auth.authenticate(email = email, username = username)
            if user:
                infomation['userExist'] = True
                return JsonResponse(infomation)
            user = User.objects.create_user(username = username, password = password, email = email)
            user.save()
            infomation['isLogin'] = True
            infomation['username'] = username
            auth.login(request,user)
            request.session['username'] = username
            return JsonResponse(infomation)
        else:
            return JsonResponse(infomation)
    return JsonResponse(infomation)

# 用于跳转页面的渲染
info = {'now_title':'Jump',
        'logo_url':'../static/image/logo.png',
        'address':'/index'}

# 从ajax中获取登录信息
@csrf_exempt
def getSignIn(request):
    infomation = {'isLogin':False}
    if request.method=='POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username = username, password = password)
            if user or user.is_authenticated:
                infomation['isLogin'] = True
                infomation['username'] = username
                request.session['username'] = username
                auth.login(request,user)
                return JsonResponse(infomation)
    return JsonResponse(infomation)

# 跳转模块
@csrf_exempt
def Jump(request):
    info['tips_infomation'] = "您好，" + str(request.user) 
    return render(request, "Jump.html", info)

# 登出模块
def doLogOut(request):
    if request.method=="GET":
        auth.logout(request)
        return JsonResponse({'logOut':True})
    return JsonResponse({'logOut':False})

# 用户页面的视图
def user(request,user):
    user_contents = {"now_title":"User"}
    user_contents = {"now_user":request.user}
    seen_movie_info=[]
    seen_movies=UserMovie.objects.filter(user_name__exact=request.user, movie_tag__exact='seen')
    for x in seen_movies:
        now_movie=Movie.objects.filter(title__exact=x.movie_title)[0]
        now_movie_info={}
        now_movie_info['id']=now_movie.image_id
        now_movie_info['picture']="poster/"+now_movie.image_id+".jpg"
        now_movie_info['title']=now_movie.title
        now_movie_info['score']=now_movie.score
        now_movie_info['type']=now_movie.types
        now_movie_info['country']=now_movie.country
        seen_movie_info.append(now_movie_info)
    user_contents['seen_movie_list']=seen_movie_info
    like_movie_info=[]
    liked_movies=UserMovie.objects.filter(user_name__exact=request.user, movie_tag__exact='liked')
    for x in liked_movies:
        now_movie=Movie.objects.filter(title__exact=x.movie_title)[0]
        now_movie_info={}
        now_movie_info['id']=now_movie.image_id
        now_movie_info['picture']="poster/"+now_movie.image_id+".jpg"
        now_movie_info['title']=now_movie.title
        now_movie_info['score']=now_movie.score
        now_movie_info['type']=now_movie.types
        now_movie_info['country']=now_movie.country
        like_movie_info.append(now_movie_info)
    user_contents['favourite_movie_list']=like_movie_info
    user_contents['recommend_movie_list']=signmovie.simpleRecommend(seen_movie_info, like_movie_info)
    return render(request,'User.html',dict(user_contents, **signmovie.contents))
