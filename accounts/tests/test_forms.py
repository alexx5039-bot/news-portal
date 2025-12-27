from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import (
    RedactorCreationForm,
    RedactorUpdateForm,
)

User = get_user_model()


class RedactorCreationFormTest(TestCase):

    def test_form_valid(self):
        form = RedactorCreationForm(data={
            "username": "john",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "years_of_experience": 10,
        })
        self.assertTrue(form.is_valid())

    def test_years_of_experience_too_big(self):
        form = RedactorCreationForm(data={
            "username": "john",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "years_of_experience": 100,
        })
        self.assertFalse(form.is_valid())

    def test_years_of_experience_negative(self):
        form = RedactorCreationForm(data={
            "username": "john",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "years_of_experience": -1,
        })
        self.assertFalse(form.is_valid())


class RedactorUpdateFormTest(TestCase):

    def test_years_of_experience_validation(self):
        user = User.objects.create_user(
            username="john",
            password="test12345"
        )

        form = RedactorUpdateForm(
            instance=user,
            data={
                "username": "john",
                "years_of_experience": 200,
            }
        )

        self.assertFalse(form.is_valid())
