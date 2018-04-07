from django.shortcuts import render
from Movies import movie as signmovie
from Movies.models import Movie
import random
import os

# Create your views here.

def signIn(request):
    signin_contents = {"now_title":"Sign_in","user_id":"Userid","password":"Password"}
    return render(request,'Sign_in.html',dict(signin_contents,**signmovie.contents))

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
        now_movie['movie_show_' + str(i+1)] = "海报/" + now_movie_info.image_id + ".jpg"
        now_movie['movie_show_' + str(i+1) + '_title'] = now_movie_info.title
        now_movie['movie_show_' + str(i+1) + '_score'] = now_movie_info.score
        now_movie['movie_show_' + str(i+1) + '_type'] = now_movie_info.types
        now_movie['movie_show_' + str(i+1) + '_country'] = now_movie_info.country
    if str(request.user)=="AnonymousUser":
        return render(request,'Index.html',dict(now_movie,**signmovie.contents))
    now_movie['now_user'] = request.user
    return render(request,'Index_User.html',dict(now_movie, **signmovie.contents))

def signUp(request):
    signup_contents = {"now_title":"Sign_up","user_id":"Userid","password1":"Password","email":"Email","password2":"ConfirmPassword"}
    return render(request,'Sign_up.html',dict(signup_contents,**signmovie.contents))