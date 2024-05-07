# added by Allan

# HttpResponse is used to
# pass the information 
# back to view
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import json
 
# Defining a function which
# will receive request and
# perform task depending 
# upon function definition
def render_home (request) :

    # string as HttpResponse
    return HttpResponse("This is the home page!")

def create_user (request):

    data = json.loads(request.body)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return JsonResponse({'error': 'Missing parameters in body'}, status=400)
    
    try:
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return JsonResponse({'message': 'User successfully created!'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)