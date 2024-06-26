# polls routes or urls


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # polls urls
    # path('polls/create', views.create_polls, name='polls.create'),
    path('polls/store', views.store_polls, name='polls.store'),
    path('polls/<int:id>/questions',views.manage_questions, name='polls.questions.manage'), # questions managment url
    path('possibilities',views.possibilities, name='possibilities'), #  possibilities url
    path('polls', views.polls, name='polls.index'),
    
    # participants urls
    path('participants', views.participants, name='participants.index'), 
    path('participants/<int:id>/delete', views.participant_delete, name='participants.delete'),
    
    # share urls
    path('polls/<int:id>/share', views.share_poll, name='polls.share'),
    
    # responses urls
    path('r/<uuid:token>/<uuid:key>', views.respond_poll, name='polls.respond'),
    path('r/<uuid:token>/<uuid:key>/responses/store', views.save_one, name='polls.responses.save'),
    
    # statistics urls
    path('statistics', views.stats, name='statistics'),
    path('polls/<int:id>/statistics/data', views.stats_data, name='poll.statistics')
]