from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.IntegerField()
    reciever = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"message from {self.sender} to {self.reciever}"