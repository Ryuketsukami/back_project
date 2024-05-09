from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class MessageSerializer(serializers.ModelSerializer):

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user.username

    class Meta:
        model = Message
        fields = ('sender', 'receiver', 'message', 'subject', 'creation_date')
    

    def validate_sender(self, value):

        current_user = self.context.get('request', None).user.username

        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('The sender username does not exist.')
        
        # We check if the sender is the current user logged in

        if current_user != value.username:
            raise PermissionError(f'You do not have permission to send a message on behalf of others., you are {value}, they are {current_user}')

        return value

    def validate_receiver(self, value):
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('The receiver username does not exist.')
        return value
    
    # POST request
    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        message.save()

        return message


