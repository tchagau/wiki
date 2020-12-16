from django.urls import path
from django.conf.urls import url

from . import views


#app_name = "encyclopedia"

urlpatterns = [
    
    
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("edit/<title>/", views.edit, name="edit"),
    path("rando/", views.rando, name="rando"),
    path("<title>/", views.detail, name="detail"),
    
    
    
    #url(r'^search/$', views.search, name='search'),
    #path("search/<title>/", views.search, name="search"),
    #path("", views.index, name="index"),

]
