from django.contrib.auth import get_user_model
from django.test import TestCase
from newspaper.forms import NewspaperForm
from django.utils import timezone
from newspaper.models import Topic

User = get_user_model()


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
            "published_date": timezone.now().date(),
            "topic": topic.id,
            "publishers": [redactor.id]
        })
        self.assertTrue(form.is_valid())

        newspaper = form.save()
        self.assertEqual(newspaper.title, "football")
        self.assertIn(redactor, newspaper.publishers.all())