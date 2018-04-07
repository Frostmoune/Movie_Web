from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.TextField()
    score = models.CharField(max_length = 4)
    diretor = models.TextField()
    screenwriter = models.TextField()
    actor = models.TextField()
    website = models.TextField()
    country = models.TextField()
    language = models.TextField()
    types = models.TextField()
    date = models.TextField()
    length = models.TextField()
    name = models.TextField()
    imdb = models.TextField()
    episodes = models.TextField()
    length_episodes = models.TextField()
    search_tag = models.CharField(max_length = 5)
    image_id = models.CharField(max_length = 7)