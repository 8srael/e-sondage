# polls routes or urls


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('polls/create', views.create_polls, name='polls.create'),
    path('polls/store', views.store_polls, name='polls.store')
]