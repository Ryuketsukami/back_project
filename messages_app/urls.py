from django.urls import path
#now import the views.py file into this code
from . import views

urlpatterns=[
   path('message/post/', views.write_messsage),
   path('message/getall/<str:username>/', views.get_all_messages),
   path('message/getallunread/<str:username>/', views.get_all_unread_messages),
   path('message/read/<str:username>/', views.read_message),
   path('message/delete/', views.delete_message)
]

#<str:username>/