from django.db import models
from accounts.models import User
# Create your models here.

class Friendship(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('declined','Declined')
    ]
    user = models.ForeignKey(User,related_name="added",on_delete=models.CASCADE)
    friend = models.ForeignKey(User,related_name="recieved",on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
    def accept(self):
        self.status = 'accepted'
        self.save()

    def decline(self):
        self.status = 'declined'
        self.save()


    def __str__(self):
        return f"{self.user.first_name} -> {self.friend.first_name} ({self.status})"

