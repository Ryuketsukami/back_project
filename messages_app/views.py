from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class MessageView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_messages(request):

    user_id = request.user.id

    if not user_id:
        return Response({'error': 'Invalid user'}, status=400)

    try:
        res_data = list(Message.objects.filter(sender=user_id).values())

        # it's okay to return an empty list instead of raising an error.
        return Response(res_data)
    except (KeyError, AttributeError) as e:
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        return Response({'error': f'An error occurred while retrieving messages: {e}'}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_unread_messages(request):

    user_id = request.user.id

    if not user_id:
        return Response({'error': 'Invalid user'}, status=400)

    try:
        res_data = list(Message.objects.filter(sender=user_id, unread=True).values())
        return Response(res_data)
    except (KeyError, AttributeError) as e:
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        return Response({'error': f'An error occurred while retrieving messages: {e}'}, status=500)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def read_message(request):

    user_id = request.user.id

    if not user_id:
        return Response({'error': 'Invalid user'}, status=400)

    try:
        message = Message.objects.filter(receiver=user_id, unread=True).first()

        if not message:
            return Response(None, safe=False)

        message.unread = False
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data)
        
    except (KeyError, AttributeError) as e:
        return Response({'error': str(e)}, status=400)
    except Exception as e:
        return Response({'error': f'An error occurred while retrieving messages: {e}'}, status=500)


@api_view(['DELETE', 'GET'])
@permission_classes([IsAuthenticated])
def delete_message(request, message_id):

    user = request.user
    
    if not user:
        return Response({'error': 'User Error: failed to get user from request'}, status=400)
    
    if not message_id:
        return Response({'error': 'Empty message_id'}, status=400)
    
    try:
        message = get_object_or_404(Message, id=message_id)
        if message.sender == user or message.receiver == user:
            message.delete()
            return Response({'success': True, 'message': 'Message successfully deleted.'})
        return Response({'error': f'You are not the sender or receiver of this message; not enough permissions'}, status=403)
    except Exception as e:
        return Response({'error': f'An error has occurred while deleting message: {e}'}, status=500)
