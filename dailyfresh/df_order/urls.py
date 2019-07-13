from django.contrib import admin
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$',views.order),
    url(r'^order_handle&',views.order_handle),
]