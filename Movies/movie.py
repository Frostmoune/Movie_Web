from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse
from .models import Movie,Comment,UserMovie
from collections import OrderedDict
from django.views.decorators.csrf import csrf_exempt
import time
import json
import random
import os
import re

path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/').replace("Movies",'Sign')

contents = {'sign_in':'/signIn/',
            'sign_up':'/signUp/',
            'index':'/index/',
            'logo_url':'../static/image/logo.png',
            'user_url':'../static/image/user.png'}

tags = ['大陆电影','美国电影','香港电影','台湾电影','日本电影','韩国电影','英国电影','法国电影','德国电影','印度电影','泰国电影',
            '剧情','爱情','喜剧','科幻','动作','悬疑','犯罪','恐怖','青春','励志','战争','文艺','黑色幽默','传记','历史','情色','暴力',
            '音乐','家庭','经典','冷门佳片','魔幻','黑帮','女性']

info_tags = {'评分':'score','导演':'diretor','编剧':'screenwriter','类型':'types',
            '主演':'actor','官方网站':'website','制片国家/地区':'country',
            '语言':'language','上映日期':'date','片长':'length',
            '又名':'name','imdb链接':'imdb','集数':'episodes','单集片长':'length_episodes'}

order_tags = OrderedDict(info_tags)

# 得到image_id地址，只在下面的loadAllInfo()中使用
def getPath(num):
    now_path = ""
    now_dir = 100000
    while now_dir>1 and num//now_dir==0:
        now_path += "0"
        now_dir //= 10 
    now_path += str(num)
    return now_path

# 将电影信息储存到数据库
def loadAllInfo():
    num = 0
    true_num = 0
    for x in tags:
        fp = open(path + "/static/items/" + x + "/" + x + ".txt","r",encoding='utf-8')
        nowtxt = str(fp.read()).split("-----------------------------------------------------------------------------------\n")
        fp.close()
        for info in nowtxt:
            if info=="" or len(info)==0 or str(info).isspace():
                break
            flag = 0
            now_info = {}
            now_title = info.split('\n',1)[0]
            now_obj = Movie.objects.filter(title__exact = now_title)
            if len(now_obj)!=0:
                flag = 1
            if flag == 0:
                now_info['title'] = info.split('\n',1)[0]
                for y in info_tags:
                    pattern = re.compile(y + '.*?\n')
                    nowtxt = re.findall(pattern, info)
                    if len(nowtxt)>0:
                        nowtxt = nowtxt[0].split(":", 1)
                        if len(nowtxt)>=2:
                            nowtxt = nowtxt[1]
                            if len(nowtxt)>=2:
                                nowtxt = nowtxt[1:-1]
                                if len(nowtxt)==0:
                                    now_info[info_tags[y]] = "无"
                                else:
                                    now_info[info_tags[y]] = nowtxt
                            else:
                                now_info[info_tags[y]] = "无"
                        else:
                            now_info[info_tags[y]] = "无"
                    else:
                        now_info[info_tags[y]] = "无"
                now_info['search_tag'] = x
                now_info['image_id'] = getPath(num)
                if Movie.objects.get_or_create(**now_info)[1]==True:
                    true_num += 1
            else:
                now_tag = str(now_obj[0].search_tag)
                if now_tag.find(x)==-1:
                    now_obj[0].search_tag += ", " + x
                    now_obj[0].save()
            num += 1
        print("Save %s finished. The total num is %d. The True number is %d."%(x, num-1, true_num-1))
  
# loadAllInfo()

@csrf_exempt
def pullMovieList(request):
    try:
        content = request.GET
        now_movie = {}
        now_tag = str(content['tag'])
        if 'isChange' in content:
            is_change = str(content['isChange']) # isChange用于判断前端页面是否已被渲染
        else:
            is_change = '1'
            now_movie['now_title'] = now_tag
        is_vis = [0 for i in range(550)] # 用于判断是否重复
        all_movies = Movie.objects.filter(search_tag__contains = now_tag)
        for i in range(12):
            if now_tag!="All":
                now_type = now_tag # 若不为All，说明已经确定了类型
            else:
                now_type = tags[random.randint(0,34)] # 否则，在35种类型中随机选一种
                all_movies = Movie.objects.filter(search_tag__contains = now_type) # 找到所有符合对应类型的电影
            length = len(all_movies)
            now_num = random.randint(0, length-1)
            now_movie_info = all_movies[now_num]
            while is_vis[now_num]==1 or now_movie_info.score=="无" or float(now_movie_info.score)<7: # 在相应的类型中找到评分大于7的电影
                now_num = random.randint(0, length-1)
                now_movie_info = all_movies[now_num]
            is_vis[now_num] = 1
            # 传递给前端页面用于渲染的信息
            now_movie['movie_show_' + str(i+1)] = "poster/" + now_movie_info.image_id + ".jpg"
            now_movie['movie_show_' + str(i+1) + '_id'] = now_movie_info.image_id
            now_movie['movie_show_' + str(i+1) + '_title'] = now_movie_info.title
            now_movie['movie_show_' + str(i+1) + '_score'] = now_movie_info.score
            now_movie['movie_show_' + str(i+1) + '_type'] = now_movie_info.types
            now_movie['movie_show_' + str(i+1) + '_country'] = now_movie_info.country
        if request.method=='POST' and str(request.user)!="AnonymousUser":
            if len(UserMovie.objects.filter(user_name__exact=request.user, movie_title__exact=request.POST['movie_title'], movie_tag__exact=request.POST['tag']))==0:
                UserMovie.objects.create(user_name=request.user, movie_title=request.POST['movie_title'], movie_tag=request.POST['tag'])
        if is_change=='1':
            if str(request.user)=="AnonymousUser": # 用于判断当前页面的用户是否为匿名用户
                return render_to_response('Index.html',dict(now_movie, **contents))
            now_movie['now_user'] = request.user
            return render_to_response('Index_User.html',dict(now_movie, **contents))
        else:
            return JsonResponse(now_movie) # 若已被渲染，则发送Json到前端
    except Exception as e:
        print(e)
        return render_to_response(None)

@csrf_exempt
def showPerMovie(request, id):
    now_movie = Movie.objects.filter(image_id__exact = id)[0]
    other_info = {'index':'/index/',
            'logo_url':'../static/image/logo.png',
            'title':now_movie.title,
            'image_id':'../static/items/poster/' + now_movie.image_id + ".jpg",
            'sign_in':'/signIn/',
            'sign_up':'/signUp/',
            'user_url':'../static/image/user.png',
            }
    movie = {}
    movie['score'] = now_movie.score
    movie['diretor'] = now_movie.diretor
    movie['screenwriter'] = now_movie.screenwriter
    movie['types'] = now_movie.types
    movie['actor'] = now_movie.actor
    movie['website'] = now_movie.website
    movie['country'] = now_movie.country
    movie['language'] = now_movie.language
    movie['date'] = now_movie.date
    movie['length'] = now_movie.length
    movie['name'] = now_movie.name
    movie['imdb'] = now_movie.imdb
    movie['episodes'] = now_movie.episodes
    movie['length_episodes'] = now_movie.length_episodes
    return_dict = {
        'Info':json.dumps(movie),
    }
    if request.method=='POST' and str(request.user)!="AnonymousUser":
        if request.POST['comment_flag']=='t':
            Comment.objects.create(user_name=request.user, content=request.POST['post_comment'], movie_name=now_movie.title)
        else:
            if len(UserMovie.objects.filter(user_name__exact=request.user, movie_title__exact=request.POST['movie_title'], movie_tag__exact=request.POST['tag']))==0:
                UserMovie.objects.create(user_name=request.user, movie_title=request.POST['movie_title'], movie_tag=request.POST['tag'])
    comment_list=Comment.objects.filter(movie_name__exact = now_movie.title)
    post_comment = []
    for x in comment_list:
        now_comment={}
        now_comment['user_name']=str(x.user_name)
        now_comment['content']=str(x.content)
        now_comment['date']=x.date
        now_comment['user_image_url']='../static/image/user.png'
        post_comment.append(now_comment)
    if len(post_comment) > 0:
        return_dict['comment_list'] = post_comment
    return_dict['movie_title'] = now_movie.title
    if str(request.user)=="AnonymousUser":
        return_dict['Other'] = json.dumps(other_info)
        return render(request, 'Movie.html', return_dict)
    else:
        other_info['now_user'] = str(request.user)
        return_dict['Other'] = json.dumps(other_info)
        return render(request, 'Movie_User.html', return_dict)

# 简单电影推荐
def simpleRecommend(seen, liked):
    types_dict = {}
    country_dict = {}
    types_total_scores = 0
    country_total_scores = 0
    movies_set = set()
    for liked_movie in liked:
        now_types = liked_movie['type'].split("/")
        now_countries = liked_movie['country'].split("/")
        for now_type in now_types:
            if not now_type.strip() in types_dict.keys():
                types_dict[now_type.strip()] = 2
                for movie in Movie.objects.filter(types__icontains = now_type.strip()):
                    movies_set.add(movie)
            else:
                types_dict[now_type.strip()] += 2
            types_total_scores += 2
        for now_country in now_countries:
            if not now_country.strip() in country_dict.keys():
                types_dict[now_country.strip()] = 2
                for movie in Movie.objects.filter(country__icontains = now_country.strip()):
                    movies_set.add(movie)
            else:
                types_dict[now_country.strip()] += 2
            country_total_scores += 2

    for seen_movie in seen:
        now_types = seen_movie['type'].split("/")
        now_countries = seen_movie['country'].split("/")
        for now_type in now_types:
            if not now_type.strip() in types_dict.keys():
                types_dict[now_type.strip()] = 1
                for movie in Movie.objects.filter(types__icontains = now_type.strip()):
                    movies_set.add(movie)
            else:
                types_dict[now_type.strip()] += 1
            types_total_scores += 1
        for now_country in now_countries:
            if not now_country.strip() in country_dict.keys():
                types_dict[now_country.strip()] = 1
                for movie in Movie.objects.filter(country__icontains = now_country.strip()):
                    movies_set.add(movie)
            else:
                types_dict[now_country.strip()] += 1
            country_total_scores += 1
    if len(movies_set) >= 60:
        select_movies = random.sample(movies_set, 60)
    else:
        select_movies = []
    movie_scores = {}
    for movie in select_movies:
        now_types = movie.types.split("/")
        now_countries = movie.country.split("/")
        if movie.score.strip() != "无":
            now_score = float(movie.score.strip()) / 10
        else:
            now_score = 0
        type_score, country_score = 0, 0
        for now_type in now_types:
            if now_type.strip() in types_dict:
                type_score += types_dict[now_type.strip()] / types_total_scores
        for now_country in now_countries:
            if now_country.strip() in country_dict:
                country_score += types_dict[now_country.strip()] / country_total_scores
        movie_scores[movie] = now_score * 10 + type_score * 6 + country_score * 3

    movie_info = []
    num = 0
    for now_movie, score in sorted(movie_scores.items(), key = lambda x:x[1], reverse = True):
        if num >= 6:
            break
        now_movie_info={}
        now_movie_info['id']=now_movie.image_id
        now_movie_info['picture']="poster/"+now_movie.image_id+".jpg"
        now_movie_info['title']=now_movie.title
        now_movie_info['score']=now_movie.score
        now_movie_info['type']=now_movie.types
        now_movie_info['country']=now_movie.country
        movie_info.append(now_movie_info)
        num += 1
    return movie_info

def getTagMovie(user, now_tag):
    movies = UserMovie.objects.filter(user_name__exact=user, movie_tag__exact=now_tag)
    movies_info = []
    for x in movies:
        now_movie=Movie.objects.filter(title__exact=x.movie_title)[0]
        now_movie_info={}
        now_movie_info['id']=now_movie.image_id
        now_movie_info['picture']="poster/"+now_movie.image_id+".jpg"
        now_movie_info['title']=now_movie.title
        now_movie_info['score']=now_movie.score
        now_movie_info['type']=now_movie.types
        now_movie_info['country']=now_movie.country
        movies_info.append(now_movie_info)
    return movies_info

def updateUserMovie(request):
    if request.method == "GET":
        now_tag = str(request.path).split("/")[2]
        movies_info = getTagMovie(request.user, now_tag)
        return JsonResponse({'More':movies_info})
    return None

def changeRecommend(request):
    if request.method == "GET":
        seen_movies = getTagMovie(request.user, 'seen')
        liked_movies = getTagMovie(request.user, 'liked')
        return JsonResponse({'Changed':simpleRecommend(seen_movies, liked_movies)})