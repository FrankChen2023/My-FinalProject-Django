from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('volume/', views.volume, name='volume'),
    path('index/<str:volume>', views.index, name='index'),
    path('data/<str:volume>/<str:session>', views.data, name='data'),
    path('source/<str:volume>/<str:session>/<str:filename>', views.source, name='source'),
    path('edit/<str:volume>/<str:session>', views.edit, name='edit'),
    path('transcription/', views.transcription, name='transcription'),
    path('delete/<str:volume>/<str:session>', views.delete, name='delete'),
    path('upload/<str:volume>/<str:session>', views.upload, name='upload'),
    path('success/<str:volume>/<str:session>', views.success, name='success'),
    path('create/', views.create, name='create'),
    path('search/<str:target>', views.search, name='search'),
    path('index_page/<str:volume>', views.index_page, name='index_page'),
    ]