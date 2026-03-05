from django.shortcuts import render, get_object_or_404, redirect
from .models import Appeal
from django.contrib.auth.decorators import login_required
from .forms import AssignAdminForm

@login_required
def index(request):
    if request.user.is_staff:
        appeals = Appeal.objects.all().order_by("-created_at")
    else:
        appeals = Appeal.objects.filter(author=request.user).order_by("-created_at")

    return render(request, "Firstpage/first.html", {"appeals": appeals})

@login_required
def assign_ticket(request, pk):
    if not request.user.is_staff:
        return redirect("index")  # тільки адміни

    appeal = get_object_or_404(Appeal, pk=pk)

    if request.method == "POST":
        form = AssignAdminForm(request.POST, instance=appeal)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = AssignAdminForm(instance=appeal)

    return render(request, "Firstpage/assign_ticket.html", {"form": form, "appeal": appeal})