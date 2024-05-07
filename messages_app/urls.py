from django.urls import path
#now import the views.py file into this code
from . import views

urlpatterns=[
   path('post/', views.write_messsage),
   path('getall/<str:username>/', views.get_all_messages),
   path('getallunread/<str:username>/', views.get_all_unread_messages),
   path('read/<str:username>/', views.read_message),
   path('delete/', views.delete_message)
]

#<str:username>/