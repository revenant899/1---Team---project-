from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import HttpResponse
from appeals.models import Appeal, Comment, AdminLog
from appeals.forms import AppealForm, CommentForm
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("appeals:admin_panel")
    else:
        return redirect("appeals:user_panel")
    
@login_required
def user_panel(request):
    appeals = Appeal.objects.filter(author=request.user).order_by("-created_at")

    return render(request, "appeals/userpanel.html", {
        "appeals": appeals
    })

@staff_member_required
def admin_logs(request):
    logs = AdminLog.objects.select_related("admin", "appeal").order_by("-created_at")
    return render(request, "appeals/logs.html", {"logs": logs})

@staff_member_required
def admin_panel(request):
  
    q = request.GET.get("q", "").strip()
    appeals = Appeal.objects.all().order_by("-created_at")

    if q:
        appeals = appeals.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(category__icontains=q) |
            Q(status__icontains=q) |
            Q(author__username__icontains=q)
        ).distinct()

    paginator = Paginator(appeals, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    status_stats = Appeal.objects.values('status').annotate(count=Count('id'))
    user_stats = Appeal.objects.values('author__username').annotate(count=Count('id'))

    return render(request, "appeals/adminpanel.html", {
        "appeals": page_obj,
        "q": q,
        "page_obj": page_obj,
        "status_stats": status_stats,
        "user_stats": user_stats
    })

@login_required
def appeal_create(request):
    if request.method == "POST":
        appeal_form = AppealForm(request.POST, request.FILES)
        if appeal_form.is_valid():
            appeal = appeal_form.save(commit=False)
            appeal.author = request.user
            appeal.save()

            AdminLog.objects.create(
                admin=request.user,
                appeal=appeal,
                action="create",
                message=f"Created ticket: {appeal.title}"
           )

            return redirect("/appeals/adminpanel")
    else:
        appeal_form = AppealForm()
    return render(request, "appeals/create.html", {"form": appeal_form})

@login_required
def appeal_update(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    if request.method == "POST":
        appeal_form = AppealForm(request.POST, request.FILES, instance=appeal)
        if appeal_form.is_valid():
            updated_appeal = appeal_form.save()

            AdminLog.objects.create(
                admin=request.user,
                appeal=updated_appeal,
                action="update",
                message=f"Updated ticket: {updated_appeal.title}"
           )

            return redirect("/appeals/adminpanel")
    else:
        appeal_form = AppealForm(instance=appeal)
    return render(request, "appeals/update.html", {"form": appeal_form})

@login_required
def appeal_delete(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    title = appeal.title

    AdminLog.objects.create(
        admin=request.user,
        appeal=None,
        action="delete",
        message=f"Deleted ticket: {title}"
    )

    appeal.delete()
    return redirect("/appeals/adminpanel")

@login_required
def appeal_status(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Appeal.Status.choices):
            old_status = appeal.status
            appeal.status = new_status
            appeal.save()

            AdminLog.objects.create(
                admin=request.user,
                appeal=appeal,
                action="status_change",
                message=f"Changed status of '{appeal.title}' from {old_status} to {new_status}"
          )

@login_required
def appeal_detail(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    edit_comment_id = request.GET.get('edit')

    if request.method == "POST":
        action = request.POST.get("action")
        comment_id = request.POST.get("comment_id")

        if action == "delete" and comment_id:
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
            comment.delete()

            AdminLog.objects.create(
                admin=request.user,
                appeal=appeal,
                action="comment_delete",
                message=f"Deleted comment from ticket: {appeal.title}"
            )

            return redirect("appeals:appeal_detail", pk=appeal.pk)
        elif action == "edit" and comment_id:
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
            new_text = request.POST.get("text")
            if new_text:
                comment.text = new_text
                comment.save()

                AdminLog.objects.create(
                    admin=request.user,
                    appeal=appeal,
                    action="comment_edit",
                    message=f"Edited comment in ticket: {appeal.title}"
                )

                return redirect("appeals:appeal_detail", pk=appeal.pk)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.appeal = appeal
                comment.author = request.user
                comment.save()

                AdminLog.objects.create(
                    admin=request.user,
                    appeal=appeal,
                    action="comment_add",
                    message=f"Added comment to ticket: {appeal.title}"
                )

                return redirect("appeals:appeal_detail", pk=appeal.pk)
    else:
        form = CommentForm()

    return render(request, "appeals/detail.html", {
        "appeal": appeal,
        "form": form,
        "edit_comment_id": int(edit_comment_id) if edit_comment_id else None,
    })

@require_POST
def update_status(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    new_status = request.POST.get('status')
    if new_status in Appeal.Status.values:
        old_status = appeal.status
        appeal.status = new_status
        appeal.save()

        AdminLog.objects.create(
            admin=request.user,
            appeal=appeal,
            action="status_change",
            message=f"Changed status of '{appeal.title}' from {old_status} to {new_status}"
        )

    return redirect(request.META.get('HTTP_REFERER', 'adminpanel'))