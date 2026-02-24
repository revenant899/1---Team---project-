from django.db import models

# Create your models here.



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