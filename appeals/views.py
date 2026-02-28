from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from appeals.models import Appeal
from appeals.forms import AppealForm
from appeals.forms import CommentForm

@login_required
def admin_panel(request):
    appeals = Appeal.objects.all().order_by("-created_at")
    return render(request, "appeals/adminpanel.html", {"appeals": appeals})

@login_required
def appeal_create(request):
    if request.method == "POST":
        appeal_form = AppealForm(request.POST, request.FILES)
        if appeal_form.is_valid():
            appeal_form.save()
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
            appeal_form.save()
            return redirect("/appeals/adminpanel")
    else:
        appeal_form = AppealForm(instance=appeal)
    
    return render(request, "appeals/update.html", {"form": appeal_form})

@login_required
def appeal_delete(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    appeal.delete()
    return redirect("/appeals/adminpanel")

@login_required
def appeal_status(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Appeal.Status.choices):
            appeal.status = new_status
            appeal.save()
        return HttpResponse(status=204)
    return redirect("/appeals/adminpanel")

@login_required
def appeal_detail(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.appeal = appeal
            comment.author = request.user  
            comment.save()
            return redirect("appeals:appeal_detail", pk=appeal.pk)
    else:
        form = CommentForm()

    return render(request, "appeals/detail.html", {
        "appeal": appeal,
        "form": form
    })

from .models import Appeal, Comment
@login_required
def appeal_detail(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.appeal = appeal
                comment.author = request.user
                comment.save()
                return redirect("appeals:appeal_detail", pk=appeal.pk)

        elif action == "edit":
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.author == request.user:
                form = CommentForm(request.POST, instance=comment)
                if form.is_valid():
                    form.save()
            return redirect("appeals:appeal_detail", pk=appeal.pk)

        elif action == "delete":
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.author == request.user:
                comment.delete()
            return redirect("appeals:appeal_detail", pk=appeal.pk)

    else:
        form = CommentForm()

    #  edit яерез ?edit=id
    edit_comment_id = request.GET.get("edit")
    try:
        edit_comment_id = int(edit_comment_id)
    except (TypeError, ValueError):
        edit_comment_id = None

    return render(request, "appeals/detail.html", {
        "appeal": appeal,
        "form": form,
        "edit_comment_id": edit_comment_id,
    })