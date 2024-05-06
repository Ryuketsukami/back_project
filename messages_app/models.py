from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete = models.CASCADE, null=False)
    receiver = models.ForeignKey(User, related_name ='received_messages', on_delete=models.CASCADE, null=False)
    message = models.TextField(null=False)
    subject = models.CharField(max_length=128, null=False)
    creation_date = models.DateTimeField(default = timezone.now)
    unread = models.BooleanField(default=True)

    # in case we decide not to use list_display
    def __str__(self) -> str:
        return f'{self.subject} from:{self.sender} to:{self.receiver}'

