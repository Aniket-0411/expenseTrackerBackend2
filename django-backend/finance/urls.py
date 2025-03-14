from django.urls import path
from . import views
from .views import chat_view

urlpatterns = [
    path('chat', chat_view, name='finance_chat'),
    path('save_chat_message/', views.save_chat_message, name='save_chat_message'),
    path('get_chat_history/', views.get_chat_history, name='get_chat_history'),
    path('clear_chat_history/', views.clear_chat_history, name='clear_chat_history'),
    path('get_rasa_response/', views.get_rasa_response, name='get_rasa_response'),
    path('api/category-data/', views.get_category_data, name='api_category_data'),
    path('api/category-amount-data/', views.get_category_amount_data, name='api_category_amount_data'),
    path('api/transactions/', views.transactions_api, name='api_transactions'),
    path('accept_image/', views.accept_image, name='accept_image'),
    path('process_text_from_flask', views.process_text_from_flask, name='process_text_from_flask'),
]
