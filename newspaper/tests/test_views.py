from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from newspaper.models import Topic, Newspaper

User = get_user_model()

class BaseViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="pass1234"
        )
        self.client.login(username="admin", password="pass1234")


class NewspaperListViewTest(BaseViewTest):
    def test_list_view_status_code(self):
        response = self.client.get(
            reverse("newspaper:newspaper-list")
        )
        self.assertEqual(response.status_code, 200)

    def test_search_works(self):
        topic = Topic.objects.create(name="Tech")
        Newspaper.objects.create(
            title="AI",
            content="AI content",
            published_date="2024-01-01",
            topic=topic
        )

        response = self.client.get(
            reverse("newspaper:newspaper-list") + "?q=AI"
        )
        self.assertContains(response, "AI")

    def test_search_filters_results(self):
        topic = Topic.objects.create(name="Tech")

        Newspaper.objects.create(
            title="AI",
            content="AI content",
            published_date="2024-01-01",
            topic=topic
        )
        Newspaper.objects.create(
            title="Sport",
            content="Football",
            published_date="2024-01-01",
            topic=topic
        )

        response = self.client.get(
            reverse("newspaper:newspaper-list") + "?q=AI"
        )

        self.assertContains(response, "AI")
        self.assertNotContains(response, "Sport")

    def test_filter_by_topic(self):
        topic_tech = Topic.objects.create(name="Tech")
        topic_sport = Topic.objects.create(name="Sport")

        tech_news = Newspaper.objects.create(
            title="AI",
            content="AI content",
            published_date="2024-01-01",
            topic=topic_tech
        )
        sport_news = Newspaper.objects.create(
            title="Football",
            content="Sport content",
            published_date="2024-01-01",
            topic=topic_sport
        )
        response = self.client.get(
            reverse("newspaper:newspaper-list"),
            {"topic": topic_tech.id}
        )
        self.assertContains(response, tech_news.title)
        self.assertNotContains(response, sport_news.title)

    def test_filter_by_redactor(self):
        topic = Topic.objects.create(name="Tech")

        redactor_1 = User.objects.create_user(
            username="john",
            password="pass1234"
        )
        redactor_2 = User.objects.create_user(
            username="anna",
            password="pass1234"
        )
        news_1 = Newspaper.objects.create(
            title="AI",
            content="AI content",
            published_date="2024-01-01",
            topic=topic
        )
        news_1.publishers.add(redactor_1)

        news_2 = Newspaper.objects.create(
            title="ML",
            content="ML content",
            published_date="2024-01-01",
            topic=topic
        )
        news_2.publishers.add(redactor_2)

        response = self.client.get(
            reverse("newspaper:newspaper-list"),
            {"redactor": redactor_1.id}
        )

        self.assertContains(response, news_1.title)
        self.assertNotContains(response, news_2.title)

    def test_filter_by_topic_and_redactor(self):
        topic = Topic.objects.create(name="Tech")
        other_topic = Topic.objects.create(name="Sport")

        redactor = User.objects.create_user(
            username="john",
            password="pass1234"
        )
        correct_news = Newspaper.objects.create(
            title="AI",
            content="AI content",
            published_date="2024-01-01",
            topic=topic
        )
        correct_news.publishers.add(redactor)

        wrong_news = Newspaper.objects.create(
            title="Football",
            content="Sport content",
            published_date="2024-01-01",
            topic=other_topic
        )
        response = self.client.get(
            reverse("newspaper:newspaper-list"),
            {
                "topic": topic.id,
                "redactor": redactor.id
            }
        )

        self.assertContains(response, correct_news.title)
        self.assertNotContains(response, wrong_news.title)



class LoginRequiredTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("newspaper:newspaper-list")
        )
        self.assertEqual(response.status_code, 302)
