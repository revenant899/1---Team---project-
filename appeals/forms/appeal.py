from django import forms
from appeals.models import Appeal

class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = [
            "title",
            "description",
            "category",
            "image",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }