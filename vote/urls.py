from django.urls import path
from . import views

app_name = 'vote'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/<vpk>', views.detail, name='detail'),
    path('vote/<vpk>', views.vote, name='vote'),
    path('cancel/<vpk>', views.cancel, name='cancel'),
    path('create/', views.create, name='create')
]