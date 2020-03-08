from django.urls import path
from . import views

app_name = 'query'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('tips/name=<str:user_name>', views.tips, name='tips'),
    path('q_id=<int:question_id>&name=<str:user_name>', views.questions, name='questions'),
    path('thanks/', views.thanks, name='thanks'),
]
