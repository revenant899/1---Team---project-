from django.contrib import admin
from .models import Appeal

@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "author", "assigned_admin", "created_at")
    list_filter = ("status", "author", "assigned_admin")
    search_fields = ("title", "description", "author__username")