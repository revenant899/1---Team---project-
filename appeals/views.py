from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
            appeal = appeal_form.save(commit=False)
            appeal.author = request.user
            appeal.save()
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

@login_required
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

    return render(request, "appeals/adminpanel.html", {"appeals": appeals, "q": q})
