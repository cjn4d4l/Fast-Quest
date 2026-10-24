from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name="home"),
    path('create_question/', views.create_question),
    path('create_user/', views.create_user),
    path('usercreate/', views.user_create),
    path('login_user/', views.login_user),
    path('userlogin/', views.user_login),
    path('userlogout/', views.user_logout),
    path("get_question/", views.get_question),
    path("delete_question/<int:question_id>/", views.delete_question),
    path("get_all_questions/", views.get_all_questions),
    path("questions/", views.view_all_questions),
]
