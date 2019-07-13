"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url, include
from df_goods import views
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include(('df_user.urls'), namespace='df_user')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^goods/', include(('df_goods.urls'), namespace='df_goods')),
    url(r'^$', views.index),
    url(r'^cart/', include('df_cart.urls')),
    url(r'^order/',include('df_order.urls')),
    url(r'^search/', include('haystack.urls')),
]