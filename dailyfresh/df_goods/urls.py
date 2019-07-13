from django.conf.urls import url,include
from . import views

app_name='[df_goods]'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.list),
    url(r'(\d+)/$', views.detail),
]