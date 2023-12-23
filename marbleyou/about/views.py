from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from product.views import QuestionFormMixin


def page_404(request, exception):
    return render(request, 'about/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'about/403csrf.html', status=403)


def page_500(request):
    return render(request, 'about/500.html', status=500)


class ContactsView(TemplateView, QuestionFormMixin):
    template_name = 'about/contacts.html'
    success_url = reverse_lazy('about:contacts')
