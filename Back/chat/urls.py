# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('message/', views.chat_message, name='chat_message'),
    path('history/', views.conversation_history, name='conversation_history'),
]