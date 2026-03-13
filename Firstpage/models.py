from django.db import models
from django.contrib.auth.models import User

class Appeal(models.Model):

    class Status(models.TextChoices):
        NOT_REVIEWED = "not_reviewed", "Not reviewed"
        CONSIDERED = "considered", "Considered"
        REJECTED = "rejected", "Rejected"

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_REVIEWED
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='firstpage_appeals')
    assigned_admin = models.ForeignKey(User, on_delete=models.SET_NULL,
                                       related_name="assigned_tickets",
                                       null=True, blank=True)

    def __str__(self):
        return self.title