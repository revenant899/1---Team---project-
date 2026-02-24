from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from appeals.models import Appeal
from appeals.forms import AppealForm


def admin_panel(request):
    appeals = Appeal.objects.all().order_by("-created_at")
    return render(request, "appeals/adminpanel.html", {"appeals": appeals})


def appeal_create(request):
    if request.method == "POST":
        appeal_form = AppealForm(request.POST, request.FILES)
        if appeal_form.is_valid():
            appeal_form.save()
            return redirect("/appeals/adminpanel")
    else:
        appeal_form = AppealForm()
    
    return render(request, "appeals/create.html", {"form": appeal_form})

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


def appeal_delete(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    appeal.delete()
    return redirect("/appeals/adminpanel")

def appeal_status(request, pk):
    appeal = get_object_or_404(Appeal, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Appeal.Status.choices):
            appeal.status = new_status
            appeal.save()
        return HttpResponse(status=204)
    return redirect("/appeals/adminpanel")