from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView

from .forms import RedactorCreationForm, RedactorUpdateForm

User = get_user_model()


class RedactorRegisterView(CreateView):
    form_class = RedactorCreationForm
    template_name = "accounts/redactor_register.html"
    success_url = reverse_lazy("login")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 7

    def get_queryset(self):
        queryset = User.objects.all().order_by("-years_of_experience")

        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return queryset


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = User

    def get_queryset(self):
        return User.objects.prefetch_related("newspapers")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = RedactorCreationForm


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = RedactorUpdateForm



class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("accounts:redactor-list")

