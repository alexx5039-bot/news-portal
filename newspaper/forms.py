from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxSelectMultiple

from .models import Newspaper


User = get_user_model()

class RedactorCreationForm(UserCreationForm):
    years_of_experience = forms.IntegerField(min_value=0)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "years_of_experience",
                  "password1",
                  "password2"
        )
    def clean_years_of_experience(self):
        years = self.cleaned_data.get("years_of_experience")

        if years is not None and not 0 <= years <= 80:
            raise forms.ValidationError(
                "Years of experience must be between 0 and 80"
            )
        return years


class RedactorUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "years_of_experience",
        )

    def clean_years_of_experience(self):
        years = self.cleaned_data.get("years_of_experience")

        if years is not None and not 0 <= years <= 80:
            raise forms.ValidationError(
                "Years of experience must be between 0 and 80"
            )
        return years


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
