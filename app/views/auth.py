from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from app.forms.auth import RegistrationForm
from app.models import Expense


class RegistrationView(FormView):
    template_name = 'auth/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class PersonalAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'app_html/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expenses'] = Expense.objects.filter(user=self.request.user)
        return context
