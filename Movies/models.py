from django.db import models

# Create your models here.
# 放到数据库里的电影信息模块
class Movie(models.Model):
    title = models.TextField() # 标题
    score = models.CharField(max_length = 4) # 评分
    diretor = models.TextField() # 导演
    screenwriter = models.TextField() # 编剧
    actor = models.TextField() # 演员
    website = models.TextField() # 官网
    country = models.TextField() # 国家/地区
    language = models.TextField() # 语言
    types = models.TextField() # 类型
    date = models.TextField() # 上映日期
    length = models.TextField() # 时长
    name = models.TextField() # 别的名字
    imdb = models.TextField() # imdb链接
    episodes = models.TextField() # 集数
    length_episodes = models.TextField() # 每集长度
    search_tag = models.CharField(max_length = 5) # 用于查询（根据类型）
    image_id = models.CharField(max_length = 7) # 对应的海报id