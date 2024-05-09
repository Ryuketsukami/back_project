from django.urls import path
from . import views
from .views import MessageView

urlpatterns=[
   path('post/', MessageView.as_view(), name='create_message'),
   path('getall/', views.get_all_messages),
   path('getallunread/', views.get_all_unread_messages),
   path('read/', views.read_message),
   path('delete/<str:message_id>/', views.delete_message)
]
