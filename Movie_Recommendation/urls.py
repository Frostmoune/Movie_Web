"""Movie_Recommendation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Sign import views as signviews
from Movies import movie as signmovie
from Sign import sign

urlpatterns = [
    # 不同的请求地址对应不同的函数
    path('admin/', admin.site.urls),
    path('index/', signviews.index),
    path('signIn/', signviews.signIn),
    path('signUp/', signviews.signUp),
    path('index/', signmovie.pullMovieList),
    path('index/movie_list', signmovie.pullMovieList),
    path('signUp/sign_up_form', sign.getSignUp),
    path('signIn/sign_in_form', sign.getSignIn),
    path('signUp/jump', sign.Jump),
    path('signIn/jump', sign.Jump),
    path('index/logOut', sign.doLogOut),
    path('movie/logOut', sign.doLogOut),
    path('movie/<str:id>', signmovie.showPerMovie),
    path('user/<str:user>',sign.user)
]
