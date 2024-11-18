from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.models import Blog
from newsletter.services import get_newsletter_from_cashe
from newsletter.forms import NewsletterForm, MessageForm, ClientForm, NewsletterManagerForm
from newsletter.models import Newsletter, Message, Client, MailingAttempt


#  CRUD для рассылок:
class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    def get_queryset(self):
        """Кеширует список рассылок на главной странице"""
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return get_newsletter_from_cashe(queryset)

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
        if self.request.user.has_perm('newsletter.can_view_newsletters'): # если пользователь модератор, то он получает другой кверисет
            context_data['object_list'] = Newsletter.objects.all()

        return context_data


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

    def get_form_kwargs(self):
        """Получить аргументы формы"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NewsletterUpdateView(UpdateView):
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

    def get_form_kwargs(self):
        """Получить аргументы формы"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NewsletterDeleteView(DeleteView):
    model = Newsletter
    success_url = reverse_lazy('newsletter:newsletter_list')


# CRUD для сообщений:
class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        """Пользователь может видеть только свои сообщения"""
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


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
class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        """Пользователь может видеть только своих клиентов"""
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=self.request.user)
        return queryset


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
