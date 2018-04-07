from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import JsonResponse
from .models import Movie
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

def getPath(num):
    now_path = ""
    now_dir = 100000
    while now_dir>1 and num//now_dir==0:
        now_path += "0"
        now_dir //= 10 
    now_path += str(num)
    return now_path

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
            now_info = {}
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
            num += 1
        print("Save %s finished. The total num is %d. The True number is %d."%(x, num-1, true_num-1))
  
# loadAllInfo()

def pullMovieList(request):
    try:
        content = request.GET
        now_movie = {}
        now_tag = str(content['tag'])
        if 'isChange' in content:
            is_change = str(content['isChange'])
        else:
            is_change = '1'
            now_movie['now_title'] = now_tag
        is_vis = [0 for i in range(550)]
        for i in range(12):
            if now_tag!="All":
                now_type = now_tag
            else:
                now_type = tags[random.randint(0,34)]
            all_movies = Movie.objects.filter(search_tag__exact = now_type)
            length = len(all_movies)
            now_num = random.randint(0,length-1)
            now_movie_info = all_movies[now_num]
            while is_vis[now_num]==1 or now_movie_info.score=="无" or float(now_movie_info.score)<7:
                now_num = random.randint(0,length-1)
                now_movie_info = all_movies[now_num]
            is_vis[now_num] = 1
            now_movie['movie_show_' + str(i+1)] = "海报/" + now_movie_info.image_id + ".jpg"
            now_movie['movie_show_' + str(i+1) + '_title'] = now_movie_info.title
            now_movie['movie_show_' + str(i+1) + '_score'] = now_movie_info.score
            now_movie['movie_show_' + str(i+1) + '_type'] = now_movie_info.types
            now_movie['movie_show_' + str(i+1) + '_country'] = now_movie_info.country
        if is_change=='1':
            if str(request.user)=="AnonymousUser":
                return render_to_response('Index.html',dict(now_movie, **contents))
            now_movie['now_user'] = request.user
            return render_to_response('Index_User.html',dict(now_movie, **contents))
        else:
            return JsonResponse(now_movie)
    except Exception as e:
        print(e)
        return render_to_response(None)