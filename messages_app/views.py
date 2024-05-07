from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Message
import json

# Create your views here.

# the layour of the request is 


def write_messsage(request):

    # add user authentication, the return should be 401 return JsonResponse({'error': 'Invalid credentials'}, status=401), if authenticated but invalid permission return 403


    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # must have a valid and authorized account in order to write a message
    auth_header = request.headers.get('Authorization')

    data = json.loads(request.body)

    if not auth_header:
        return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)

    if not data.get('sender') or not data.get('receiver'):
        # check if sender is authorized, check if both sender and receiver exist
        return JsonResponse({'error': 'Invalid sender or receiver'}, status=400)
    
    if not data.get('message') or not data.get('subject') or len(data.get('subject')) > 128:
        return JsonResponse({'error': 'Invalid message or subject'}, status=400)

    message = Message(
        sender=data.get('sender'),
        receiver=data.get('receiver'),
        message=data.get('message'),
        subject=data.get('subject'),
    )

    try:
        message.save()
        return JsonResponse({'message': 'Message sent successfully'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    


def get_all_messages(request, username):

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)

    if not username:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    # authentication logic needs to be added

    res_data = list(Message.objects.filter(username).values())
    return JsonResponse(res_data, safe=False)


def get_all_unread_messages(request, username):
    
    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)

    if not username:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    # authentication logic needs to be added

    try:
        res_data = list(Message.objects.filter(username, unread=True).values())
        return JsonResponse(res_data, safe=False)
    except (KeyError, AttributeError) as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while retrieving messages.'}, status=500)



def read_message(request, username):

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)

    if not username:
        return JsonResponse({'error': 'Invalid user'}, status=400)

    try:
        message_list = list(Message.objects.filter(receiver=username).values())
        if message_list:
            message_to_read = message_list[0]
            message_to_read.unread = False
            message_to_read.save()
            return JsonResponse(message_to_read, safe=False)
        return JsonResponse(None, safe=False)
    except (KeyError, AttributeError) as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An error occurred while retrieving messages: {e}'}, status=500)


def delete_message(request):

    if request.method != 'DELETE' or request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    auth_header = request.headers.get('Authorization')

    if not auth_header:
        return JsonResponse({'error': 'Invalid Authorization header format'}, status=400)
    
    data = json.loads(request.body)
    username = data.get('username')
    message = data.get('message')
    
    if not username:
        return JsonResponse({'error': 'Missing username in body'}, status=400)
    
    if not message or not message.id:
        return JsonResponse({'error': 'Missing message in body'}, status=400)
    
    try:
        message_from_db = get_object_or_404(Message, id=message.id)
        if message_from_db.sender == username or message_from_db.receiver == username:
            message_from_db.delete()
            return JsonResponse({'success': True, 'message': 'Message successfully deleted.'})
        return JsonResponse({'error': 'You are not the sender or receiver of the message; Not enough permissions.'}, status=403)
    except Exception as e:
        return JsonResponse({'error': f'An error has occurred while deleting message: {e}'}, status=500)
