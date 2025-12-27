from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils import timezone

from .models import Newspaper


class NewspaperForm(forms.ModelForm):
    class Meta:
        model = Newspaper
        fields = "__all__"
        widgets = {
            "published_date": forms.DateInput(
                attrs={"type": "date",
                       "class": "form-control"
                       }
            ),
            "topic": forms.Select(
                attrs={"class": "form-select"}
            ),
            "publishers": CheckboxSelectMultiple(
                attrs={"class": "form-check"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["topic"].empty_label = "Select topic"

    def clean_published_date(self):
        published_date = self.cleaned_data.get("published_date")
        today = timezone.now().date()

        if published_date and published_date < today:
            raise forms.ValidationError(
                "Published date cannot be in the past."
            )

        return published_date
