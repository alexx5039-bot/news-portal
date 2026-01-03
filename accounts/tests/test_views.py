from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from newspaper.models import Topic, Newspaper
from datetime import date

User = get_user_model()


class BaseRedactorViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="pass1234",
            first_name="Admin",
            last_name="User",
        )
        self.client.login(username="admin", password="pass1234")


class RedactorLoginRequiredTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse("accounts:redactor-list")
        )
        self.assertEqual(response.status_code, 302)


class RedactorListViewTest(BaseRedactorViewTest):
    def test_list_view_status_code(self):
        response = self.client.get(
            reverse("accounts:redactor-list")
        )
        self.assertEqual(response.status_code, 200)

    def test_list_contains_redactor(self):
        response = self.client.get(
            reverse("accounts:redactor-list")
        )
        self.assertContains(response, self.user.username)

    def test_search_works(self):
        User.objects.create_user(
            username="john",
            password="pass1234",
            first_name="John",
            last_name="Smith",
        )

        response = self.client.get(
            reverse("accounts:redactor-list") + "?q=john"
        )

        self.assertContains(response, "john")

    def test_search_filters_results(self):
        User.objects.create_user(
            username="john",
            password="pass1234"
        )
        User.objects.create_user(
            username="anna",
            password="pass1234"
        )

        response = self.client.get(
            reverse("accounts:redactor-list") + "?q=john"
        )

        self.assertContains(response, "john")
        self.assertNotContains(response, "anna")


class RedactorDetailViewTest(BaseRedactorViewTest):
    def test_detail_view_status_code(self):
        response = self.client.get(
            reverse("accounts:redactor-detail", args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_contains_data(self):
        response = self.client.get(
            reverse("accounts:redactor-detail", args=[self.user.pk])
        )
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.first_name)


class RedactorCreateViewTest(BaseRedactorViewTest):
    def test_create_view_status_code(self):
        response = self.client.get(
            reverse("accounts:redactor-create")
        )
        self.assertEqual(response.status_code, 200)


class RedactorUpdateViewTest(BaseRedactorViewTest):
    def test_update_view_status_code(self):
        response = self.client.get(
            reverse("accounts:redactor-update", args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 200)


class RedactorDeleteViewTest(BaseRedactorViewTest):
    def test_delete_view_status_code(self):
        response = self.client.get(
            reverse("accounts:redactor-delete", args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 200)


class NewspaperPermissionTest(TestCase):
    def setUp(self):
        self.editor1 = User.objects.create_user(
            username="editor1", password="pass1234"
        )
        self.editor2 = User.objects.create_user(
            username="editor2", password="pass1234"
        )
        self.superuser = User.objects.create_superuser(
            username="superadmin", password="pass1234"
        )
        self.topic = Topic.objects.create(name="Politics")

        self.newspaper1 = Newspaper.objects.create(
            title="News 1",
            content="Content 1",
            published_date=date.today(),
            topic=self.topic,
        )
        self.newspaper1.publishers.add(self.editor1)

        self.newspaper2 = Newspaper.objects.create(
            title="News 2",
            content="Content 2",
            published_date=date.today(),
            topic=self.topic,
        )
        self.newspaper2.publishers.add(self.editor2)

    def test_editor_can_edit_own_newspaper(self):
        self.client.force_login(self.editor1)

        response = self.client.get(
            reverse("newspaper:newspaper-update", args=[self.newspaper1.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_editor_cannot_edit_foreign_newspaper(self):
        self.client.force_login(self.editor1)

        response = self.client.get(
            reverse("newspaper:newspaper-update", args=[self.newspaper2.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_superuser_can_delete_any_newspaper(self):
        self.client.force_login(self.superuser)

        response = self.client.get(
            reverse("newspaper:newspaper-delete", args=[self.newspaper2.id])
        )

        self.assertEqual(response.status_code, 200)
