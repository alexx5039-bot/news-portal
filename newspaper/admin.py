from django.contrib import admin
from .models import Topic, Newspaper, Redactor
from django.contrib.auth.admin import UserAdmin


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "topic")
    list_filter = ("topic", "published_date")
    search_fields = ("title", "content")
    filter_horizontal = ("publishers", )


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    model = Redactor

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "years_of_experience",
        "is_staff"
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = UserAdmin.fieldsets + (
    ("Additional info", {"fields": ("years_of_experience",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
    ("Additional info", {"fields": ("years_of_experience", )}),
    )
