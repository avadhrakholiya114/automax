from django.urls import path
from . import views


urlpatterns = [
   path('', views.main_view, name='main'),
   path('home/', views.home_view, name='home'),
   path('list/', views.list_view, name='list'),
    
]