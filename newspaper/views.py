from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import Newspaper

class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    context_object_name = "newspaper_list"
    paginate_by = 6
    queryset = Newspaper.objects.select_related(
        "topic"
    ).prefetch_related("publishers")

class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail.html"
    context_object_name = "newspaper"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    fields = [
        "title",
        "content",
        "published_date",
        "topic",
        "publishers"]
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = [
        "title",
        "content",
        "published_date",
        "topic",
        "publishers"]
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    template_name = "newspaper/newspaper_confirm_delete.html"
    success_url = reverse_lazy("newspaper:newspaper-list")
