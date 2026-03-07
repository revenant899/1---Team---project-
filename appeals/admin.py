from django.contrib import admin

from .models import Appeal, Comment


@admin.register(Appeal)
class AppealAdmin(admin.ModelAdmin):

    list_display = ("title", "status", "created_at")
    list_editable = ('status',)
    list_filter = ("status",)

    search_fields = ("title", "description")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "appeal", "created_at")
    search_fields = ("text",)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0