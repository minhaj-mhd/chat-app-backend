from django.db import models
from accounts.models import User
from django.utils import timezone

# Create your models here.
class Message(models.Model):
    sender = models.IntegerField()
    reciever = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"message from {self.sender} to {self.reciever}"

class OnlineStatusTrack(models.Model):
    userOne = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracked_as_user_one")
    userTwo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tracked_as_user_two")
    user_one_checkout = models.DateTimeField(default=timezone.now)
    user_two_checkout = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('userOne', 'userTwo')