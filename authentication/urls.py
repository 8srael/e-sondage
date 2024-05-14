# authentication urls : login and register


from django.urls import path

from . import views

urlpatterns = [
    path('login_and_register/', views.login_and_register, name='login_and_register'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]