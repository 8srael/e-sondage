# polls routes or urls


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('polls/create', views.create_polls, name='polls.create'),
    path('polls/store', views.store_polls, name='polls.store'),
    path('polls/<int:id>',views.manage_questions, name='poll.questions.manage')
]