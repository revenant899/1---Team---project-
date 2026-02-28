from django.db import models
from django.conf import settings


class Appeal(models.Model):
    CATEGIRY_CHOICES = [
        ('technical_issue', 'Technical Issue'),
        ('billing_issue', 'Billing Issue'),
        ('account_issue', 'Account Issue'),
        ('other', 'Other'),
    ]

    class Status(models.TextChoices):
        NOT_REVIEWED = "not_reviewed", "Not reviewed"
        CONSIDERED = "considered", "Considered"
        REJECTED = "rejected", "Rejected"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appeals",
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGIRY_CHOICES)
    image = models.ImageField(upload_to='appeal_images/', blank=True, null=True, default=None)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_REVIEWED
    )

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User

class Comment(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment #{self.id} for Appeal #{self.appeal_id}"