# polls routes or urls


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('polls/create', views.create_polls, name='polls.create'),
    path('polls/store', views.store_polls, name='polls.store'),
    path('polls/<int:id>/questions',views.manage_questions, name='polls.questions.manage'),
    path('polls/<int:id>/share',views.share_poll, name='polls.share'),
    path('p/q/<uuid:token>', views.generate_participant_link, name='polls.participant.link'),
    path('p/q/<uuid:token>/login', views.participant_login, name='polls.participants.login'),
    path('r/<uuid:token>/<uuid:key>', views.respond_poll, name='polls.respond')
]