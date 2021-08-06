from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('form/', views.form),  # 데이터를 입력하는 주소
    path('proc/', views.proc),  # 데이터를 저장하는 주소
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name='question_create'),
]