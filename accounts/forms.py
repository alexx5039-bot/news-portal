from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class YearsOfExperienceMixin:
    def clean_years_of_experience(self):
        years = self.cleaned_data.get("years_of_experience")
        if years is not None and not 0 <= years <= 80:
            raise forms.ValidationError(
                "Years of experience must be between 0 and 80"
            )
        return years


class RedactorCreationForm(
    YearsOfExperienceMixin,
    UserCreationForm
):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "password1",
            "password2",
        )


class RedactorUpdateForm(
    YearsOfExperienceMixin,
    forms.ModelForm
):
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        )
