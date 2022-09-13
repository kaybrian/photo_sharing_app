from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.index, name='index'),
    path('singup/',views.signup, name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout, name='logout'),
    path('settings/', views.settings, name="settings"),

    # posts 
    path('upload/',views.upload, name='upload'),
    path('like-post/', views.like_post, name="like-post")
]
