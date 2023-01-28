from home.views import *
from django.urls import path,include

urlpatterns = [
  path('animals/', AnimalView.as_view()),
  path('animals/<pk>/', AnimalDetailsView.as_view()),
  path('register/',RegisterAPI.as_view()),
  path('login/',LoginAPI.as_view()),
  path('create/',AnimalCreateAPI.as_view())
]