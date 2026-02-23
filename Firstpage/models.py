from django.db import models


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

    def __str__(self):
        return self.title