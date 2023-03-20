from django.urls import path

from . import views
from get_infos.views import listproblems
urlpatterns = [
    path('problems/', listproblems),
]