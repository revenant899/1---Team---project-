from django.contrib import admin

from .models import Appeal


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):

    list_display = ("title", "status", "created_at")

    list_filter = ("status",)

    search_fields = ("title", "description")