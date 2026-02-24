from django.shortcuts import render
from appeals.models import Appeal


def index(request):
    appeals = Appeal.objects.all().order_by("-created_at")
    return render(request, "Firstpage/first.html", {"appeals": appeals})