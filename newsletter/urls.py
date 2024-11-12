from django.urls import path
from newsletter.apps import NewsletterConfig
from newsletter.views import NewsletterListView, NewsletterDetailView, NewsletterCreateView, NewsletterUpdateView, \
    NewsletterDeleteView, ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, attempts

app_name = NewsletterConfig.name

urlpatterns = [
    #  urls для рассылок:
    path('', NewsletterListView.as_view(), name='newsletter_list'),
    path('newsletter_details/<int:pk>/', NewsletterDetailView.as_view(), name='newsletter_detail'),
    path('newsletter_create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter_update/<int:pk>/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    path('newsletter_delete/<int:pk>/', NewsletterDeleteView.as_view(), name='newsletter_delete'),

    #  urls для клиентов:
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('client_details/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('client_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    #  urls для сообщений
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_details/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('attemts/', attempts, name='attempts'),
]
