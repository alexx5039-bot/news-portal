from django.contrib.auth import get_user_model
from django.test import TestCase
from newspaper.forms import (RedactorCreationForm,
                             NewspaperForm)

from newspaper.models import Topic

User = get_user_model()

class RedactorCreationFormTest(TestCase):

    def test_form_valid(self):
        form = RedactorCreationForm(data={
            "username": "john",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "years_of_experience": 10
        })
        self.assertTrue(form.is_valid())

    def test_years_of_experience_too_big(self):
        form = RedactorCreationForm(data={
            "username": "john",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "years_of_experience": 100
        })
        self.assertFalse(form.is_valid())


class NewspaperFormTest(TestCase):

    def test_form_valid(self):
        topic = Topic.objects.create(name="Sport")
        redactor = User.objects.create_user(
            username="john",
            password="pass1234"
        )
        form = NewspaperForm(data={
            "title": "football",
            "content": "News",
            "published_date": "2024-01-01",
            "topic": topic.id,
            "publishers": [redactor.id]
        })
        self.assertTrue(form.is_valid())
