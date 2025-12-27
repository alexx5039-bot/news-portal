from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from .forms import NewspaperForm
from .models import Newspaper, Topic

User = get_user_model()


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "newspaper/home.html"


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    context_object_name = "newspaper_list"
    paginate_by = 6

    def get_queryset(self):
        queryset = (
            Newspaper.objects
            .select_related("topic")
            .prefetch_related("publishers")
            .order_by("-published_date")
        )
        query = self.request.GET.get("q", "").strip()
        topic_id = self.request.GET.get("topic")
        redactor_id = self.request.GET.get("redactor")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(topic__name__icontains=query)
            )
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        if redactor_id:
            queryset = queryset.filter(publishers__id=redactor_id)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        context["redactors"] = User.objects.all().order_by("username")
        return context


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail.html"
    context_object_name = "newspaper"

    def get_queryset(self):
        return (
            Newspaper.objects
            .select_related("topic")
            .prefetch_related("publishers")
        )


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "newspaper/newspaper_form.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    template_name = "newspaper/newspaper_confirm_delete.html"
    success_url = reverse_lazy("newspaper:newspaper-list")


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "newspaper/topic_list.html"
    paginate_by = 11

    def get_queryset(self):
        queryset = (
            Topic.objects
            .annotate(newspapers_count=Count("newspapers"))
            .order_by("-newspapers_count", "name")
        )

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                name__icontains=query
            )
        return queryset


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    context_object_name = "topic"
    template_name = "newspaper/topic_detail.html"

    def get_queryset(self):
        return Topic.objects.prefetch_related("newspapers")


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = ["name"]
    template_name = "newspaper/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = ["name"]
    template_name = "newspaper/topic_form.html"
    success_url = reverse_lazy("newspaper:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    template_name = "newspaper/topic_confirm_delete.html"
    success_url = reverse_lazy("newspaper:topic-list")


