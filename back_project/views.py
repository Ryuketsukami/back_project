from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
 

def render_home (request) :

    # string as HttpResponse
    return HttpResponse("Website started!")