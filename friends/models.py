from django.db import models
from accounts.models import User
# Create your models here.

class Friendship(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('declined','Declined')
    ]
    user = models.ForiegnKey(User,related_name="added",on_delete=models.CASCADE)
    friend = models.ForiegnKey(User,related_name="recieved",on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username} ({self.status})"

