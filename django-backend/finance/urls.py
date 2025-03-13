from django.urls import path
from . import views
from .views import chat_view

urlpatterns = [
    path('chat', chat_view, name='finance_chat'),
    path('save_chat_message/', views.save_chat_message, name='save_chat_message'),
    path('get_chat_history/', views.get_chat_history, name='get_chat_history'),
    path('clear_chat_history/', views.clear_chat_history, name='clear_chat_history'),
    path('get_rasa_response/', views.get_rasa_response, name='get_rasa_response'),
]
