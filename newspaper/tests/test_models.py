from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from newspaper.models import Topic, Newspaper

User = get_user_model()


class TopicModelTest(TestCase):
    def test_str_method(self):
        topic = Topic.objects.create(name="Politics")
        self.assertEqual(str(topic), "Politics")


class RedactorModelCase(TestCase):
    def test_str_method(self):
        redactor = User.objects.create_user(
            username="john",
            password="test1234"
        )
        self.assertEqual(str(redactor), "john")

    def test_get_absolute_url(self):
        redactor = User.objects.create_user(
            username="john",
            password="test1234"
        )
        self.assertEqual(
            redactor.get_absolute_url(),
            reverse("newspaper:redactor-detail", args=[redactor.id])
        )


class NewspaperModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Tech")
        self.redactor = User.objects.create_user(
            username="editor",
            password="test1234"
        )

    def test_str_method(self):
        newspaper = Newspaper.objects.create(
            title="AI News",
            content="Some content",
            published_date="2024-01-01",
            topic=self.topic
        )

        self.assertEqual(str(newspaper), "AI News (2024-01-01)")

    def test_str_newspaper_relations(self):
        newspaper = Newspaper.objects.create(
            title="AI News",
            content="Some content",
            published_date="2024-01-01",
            topic=self.topic
        )
        newspaper.publishers.add(self.redactor)

        self.assertIn(newspaper, self.topic.newspapers.all())
        self.assertIn(newspaper, self.redactor.newspapers.all())
