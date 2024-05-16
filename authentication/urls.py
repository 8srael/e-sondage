# authentication urls : login and register


from django.urls import path

from . import views

urlpatterns = [
    path('login_and_register/', views.login_and_register, name='login_and_register'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
]