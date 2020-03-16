from django.urls import path
from . import views

app_name = 'query'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('q_id=<int:question_id>&name=<str:user_name>&environment=<str:environment>', views.questions, name='questions'),
    path('thanks/', views.thanks, name='thanks'),
]
