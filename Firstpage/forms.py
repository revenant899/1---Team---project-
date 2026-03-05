from django import forms
from .models import Appeal
from django.contrib.auth.models import User

class AssignAdminForm(forms.ModelForm):
    assigned_admin = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True), required=True)

    class Meta:
        model = Appeal
        fields = ["assigned_admin"]