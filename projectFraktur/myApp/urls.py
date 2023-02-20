from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('volume/', views.volume, name='volume'),
    path('index/<str:volume>', views.index, name='index'),
    path('data/<str:volume>/<str:minute>', views.data, name='data'),
    path('edit/<str:volume>/<str:minute>', views.edit, name='edit'),
    path('transcription/', views.transcription, name='transcription'),
    path('delete/<str:volume>/<str:minute>', views.delete, name='delete'),
    path('upload/<str:volume>/<str:minute>', views.upload, name='upload'),
    path('success/<str:volume>/<str:minute>', views.success, name='success'),
    path('create/', views.create, name='create'),
    path('search/', views.search, name='search'),
    ]