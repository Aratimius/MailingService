from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Blog
from newsletter.forms import NewsletterForm, MessageForm, ClientForm, NewsletterManagerForm
from newsletter.models import Newsletter, Message, Client, MailingAttempt
from newsletter.services import get_newsletters_from_cache


#  CRUD для рассылок:
class NewsletterListView(ListView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        """Передать объекту отчет о рассылках"""
        context_data = super().get_context_data(**kwargs)
        context_data['attempts'] = MailingAttempt.objects.all()
        context_data['letters_count'] = Newsletter.objects.all().count()
        context_data['active_letters_count'] = Newsletter.objects.filter(status='STARTED').count()
        context_data['unique_clients_conunt'] = Client.objects.values_list('email', flat=True).distinct().count()
        # 3 случайных поста:
        all_posts = list(Blog.objects.filter(publication_sign=True))
        context_data['random_posts'] = sample(all_posts, min(len(all_posts), 3))

        # сортировать по владельцу
        for object in Newsletter.objects.all():
            if object.owner == self.request.user:
                object.is_first = 1
                object.save()
            else:
                object.is_first = 0
                object.save()
        object_list = Newsletter.objects.all().order_by('-is_first')
        context_data['object_list'] = object_list

        return context_data

    def get_queryset(self):
        """Кеширует список рассылок на главной странице"""
        return get_newsletters_from_cache()


class NewsletterDetailView(DetailView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        """Передать объекту клиентов"""
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = Newsletter.objects.get(message=self.kwargs['pk']).client.all()
        return context_data


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')
    form_class = NewsletterForm

    def form_valid(self, form):
        """Добавить пользователя"""
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')
    form_class = NewsletterForm

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return NewsletterForm
        elif user.has_perm('newsletter.can_change_status'):
            return NewsletterManagerForm
        raise PermissionDenied


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')


# CRUD для сообщений:
class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    success_url = reverse_lazy('newsletter:message_list')
    form_class = MessageForm

    def form_valid(self, form):
        """Добавить пользователя"""
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    success_url = reverse_lazy('newsletter:message_list')
    form_class = MessageForm


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message_list')


# CRUD для клиентов:
class ClientListView(ListView):
    model = Client

    def get_context_data(self, *, object_list=None, **kwargs):
        context_data = super().get_context_data(**kwargs)
        for object in Client.objects.all():
            if object.owner == self.request.user:
                object.is_first = 1
                object.save()
            else:
                object.is_first = 0
                object.save()

        object_list = Client.objects.all().order_by('-is_first')
        context_data['object_list'] = object_list
        return context_data



class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')
    form_class = ClientForm

    def form_valid(self, form):
        """Добавить пользователя"""
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')
    form_class = ClientForm


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


def attempts(request):
    """Вывести отчет проведенных рассылок
    C проверкой о том, что эти попытки принадлежат к вошедшему пользователю"""
    user_mailings = []
    for newsletter in Newsletter.objects.filter(owner=request.user):
        if newsletter.owner == request.user:
            for mailing in MailingAttempt.objects.filter(newsletter=newsletter):
                user_mailings.append(mailing)
    context = {
        'attempt_list': user_mailings,  # пользователь будет видет отчет только по своим рассылкам
    }
    return render(request, 'newsletter/attempts.html', context)
