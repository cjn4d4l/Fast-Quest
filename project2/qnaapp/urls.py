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
    path("get_recents/", views.get_recents),
    path("delete_topic/<int:topic_id>/", views.delete_topic),
    path("topics/", views.view_topics),
    path("get_topics/", views.get_topics),
    path("questions/<int:topic_id>/", views.view_questions),
]
