from django.contrib import admin
from .models import AdminLog, Appeal, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ("id", "admin", "appeal", "action", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("admin__username", "message")


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "description", "author__username")
    inlines = (CommentInline,)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "appeal", "created_at")
    search_fields = ("text",)