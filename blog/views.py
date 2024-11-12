
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog
from blog.services import get_object_from_cashe


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog

    def get_queryset(self):
        """Фильтрация по опубликованным статьсям"""
        queryset = super().get_queryset()
        queryset = queryset.filter(publication_sign=True)
        return get_object_from_cashe(queryset)


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview', 'publication_sign')

    def get_success_url(self):
        """Перенаправление после редактирования на просмотр блога"""
        return reverse("blog:detail", args=[self.kwargs.get("pk")])


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """Метод для увеличения счетчика просмотров"""
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')