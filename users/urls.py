from django.urls import path

from users import views

urlpatterns = [
    path('create', views.CustomUserCreate.as_view()),
    path('comment', views.CommentCreate.as_view())
]
