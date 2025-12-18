from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse


class Topic(models.Model):
    name = CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Redactor(AbstractUser):
    years_of_experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("newspaper:redactor-detail", args=[str(self.id)])


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="newspapers"
    )
    publishers = models.ManyToManyField(
        "Redactor",
        related_name="newspapers"
    )

    def __str__(self):
        return self.title