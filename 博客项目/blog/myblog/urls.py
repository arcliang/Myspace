from django.conf.urls import url,include
from . import views

app_name='[myblog]'
urlpatterns = [
    url(r'^login/',views.login),
    url(r'^register/', views.register),
    url(r'^showlogin',views.showlogin),
    url(r'^showregister', views.showregister),
    url(r'^category/(\d+)/$', views.category),
    url(r'^index/$',views.index),
    url(r'^articledetail/(\d+)/$',views.articledetail),
    url(r'^logout/$',views.logout),
    url(r'^useredit/$',views.useredit),
    url(r'^showuseredit/$',views.showuseredit),
]
