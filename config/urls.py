"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from get_infos.views import search_prob
from get_infos.views import add_tag
from get_infos.views import problem_stats
urlpatterns = [
    path('admin/', admin.site.urls),

    # 添加如下的路由记录
    path('get_infos/search_list', search_prob),
    path('get_infos/add',add_tag),
    path('get_infos/search_stats',problem_stats)
]
