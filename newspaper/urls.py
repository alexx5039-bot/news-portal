from django.urls import path
from .views import (
    NewspaperListView,
    NewspaperDetailView,
    NewspaperCreateView,
    NewspaperDeleteView,
    NewspaperUpdateView
)


app_name = "newspaper"

urlpatterns = [
    path("", NewspaperListView.as_view(), name="newspaper-list"),
    path(
        "newspapers/<int:pk>/",
        NewspaperDetailView.as_view(),
        name="newspaper-detail"
    ),
    path(
        "newspapers/create/",
        NewspaperCreateView.as_view(),
        name="newspaper-create"
    ),
    path(
        "newspapers/<int:pk>/update/",
        NewspaperUpdateView.as_view(),
        name="newspaper-update"
    ),
    path(
        "newspapers/<int:pk>/delete/",
        NewspaperDeleteView.as_view(),
        name="newspaper-delete"
    ),
]
