from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


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

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_appeals', null=True, blank=True)

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
    

class Comment(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="comments")
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments", null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment #{self.id} for Appeal #{self.appeal_id}"

class AdminLog(models.Model):
    ACTION_CHOICES = [
    ("create", "Create"),
    ("update", "Update"),
    ("delete", "Delete"),
    ("status_change", "Status Change"),
    ("comment_add", "Comment Add"),
    ("comment_edit", "Comment Edit"),
    ("comment_delete", "Comment Delete"),

    ]

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_logs"
    )
    appeal = models.ForeignKey(
        Appeal,
        on_delete=models.SET_NULL,
        related_name="logs",
        null=True,
        blank=True
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} - {self.action} - {self.created_at:%Y-%m-%d %H:%M}"