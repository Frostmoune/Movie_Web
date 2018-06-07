from django.shortcuts import render
from Movies import movie as signmovie
from Movies.models import Movie,UserMovie
from django.views.decorators.csrf import csrf_exempt
import random
import os

# Create your views here.

# 登录页面的视图
def signIn(request):
    signin_contents = {"now_title":"Sign_in","user_id":"Userid","password":"Password"}
    return render(request,'Sign_in.html',dict(signin_contents,**signmovie.contents))

# 目录页面的视图
@csrf_exempt
def index(request):
    now_movie = {}
    length = 251
    now_movie['now_title'] = "Index"
    for i in range(12):
        now_type = signmovie.tags[random.randint(0,34)]
        all_movies = Movie.objects.filter(search_tag__exact = now_type)
        length = len(all_movies)
        now_num = random.randint(0,length-1)
        now_movie_info = all_movies[now_num]
        while now_movie_info.score=="无" or float(now_movie_info.score)<7:
            now_num = random.randint(0,length-1)
            now_movie_info = all_movies[now_num]
        now_movie['movie_show_' + str(i+1)] = "poster/" + now_movie_info.image_id + ".jpg"
        now_movie['movie_show_' + str(i+1) + '_id'] = now_movie_info.image_id
        now_movie['movie_show_' + str(i+1) + '_title'] = now_movie_info.title
        now_movie['movie_show_' + str(i+1) + '_score'] = now_movie_info.score
        now_movie['movie_show_' + str(i+1) + '_type'] = now_movie_info.types
        now_movie['movie_show_' + str(i+1) + '_country'] = now_movie_info.country
    if request.method=='POST' and str(request.user)!="AnonymousUser":
        if len(UserMovie.objects.filter(user_name__exact=request.user, movie_title__exact=request.POST['movie_title'], movie_tag__exact=request.POST['tag']))==0:
            UserMovie.objects.create(user_name=request.user, movie_title=request.POST['movie_title'], movie_tag=request.POST['tag'])
    if str(request.user)=="AnonymousUser": # 判断用户是否为匿名用户
        return render(request,'Index.html',dict(now_movie,**signmovie.contents)) # 若是，转移到给匿名用户的页面
    now_movie['now_user'] = request.user
    return render(request,'Index_User.html',dict(now_movie, **signmovie.contents)) # 若不是，转移到给用户的页面

# 登录页面的视图
def signUp(request):
    signup_contents = {"now_title":"Sign_up","user_id":"Userid","password1":"Password","email":"Email","password2":"ConfirmPassword"}
    return render(request,'Sign_up.html',dict(signup_contents,**signmovie.contents))

# 搜索页面的视图
def search(request):
    search_key = request.GET.get('search_key')
    all_movie = Movie.objects.filter(title__icontains=search_key)
    movie_list = []
    #check_same = []
    for m in all_movie:
        n={}
        n['picture']="poster/"+m.image_id+".jpg"
        n['id']=m.image_id
        n['title']=m.title
        n['score'] = m.score
        n['type'] = m.types
        n['country'] = m.country
        #if m.title not in check_same:
        movie_list.append(n)
        #check_same.append(m.title)
    if str(request.user)=="AnonymousUser": # 判断用户是否为匿名用户
        return render(request,'Search_test.html',dict({'movie_list': movie_list}, **signmovie.contents)) # 若是，转移到给匿名用户的页面
    return render(request,'Search_user.html',dict({'movie_list': movie_list, 'now_user' : request.user}, **signmovie.contents)) # 若不是，转移到给用户的页面

# 用户页面的视图
def user(request,user):
    user_contents = {"now_title":"User"}
    user_contents = {"now_user":request.user}
    seen_movie_info=[]
    seen_movies=UserMovie.objects.filter(user_name__exact=request.user, movie_tag__exact='seen')
    num = 0
    for x in seen_movies:
        if num >= 6:
            break
        now_movie=Movie.objects.filter(title__exact=x.movie_title)[0]
        now_movie_info={}
        now_movie_info['id']=now_movie.image_id
        now_movie_info['picture']="poster/"+now_movie.image_id+".jpg"
        now_movie_info['title']=now_movie.title
        now_movie_info['score']=now_movie.score
        now_movie_info['type']=now_movie.types
        now_movie_info['country']=now_movie.country
        seen_movie_info.append(now_movie_info)
        num += 1
    user_contents['seen_movie_list']=seen_movie_info
    like_movie_info=[]
    liked_movies=UserMovie.objects.filter(user_name__exact=request.user, movie_tag__exact='liked')
    num = 0
    for x in liked_movies:
        if num >= 6:
            break
        now_movie=Movie.objects.filter(title__exact=x.movie_title)[0]
        now_movie_info={}
        now_movie_info['id']=now_movie.image_id
        now_movie_info['picture']="poster/"+now_movie.image_id+".jpg"
        now_movie_info['title']=now_movie.title
        now_movie_info['score']=now_movie.score
        now_movie_info['type']=now_movie.types
        now_movie_info['country']=now_movie.country
        like_movie_info.append(now_movie_info)
        num += 1
    user_contents['favourite_movie_list']=like_movie_info
    user_contents['recommend_movie_list']=signmovie.simpleRecommend(seen_movie_info, like_movie_info)
    return render(request,'User.html',dict(user_contents, **signmovie.contents))