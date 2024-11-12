from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField
from newsletter.models import Newsletter, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class NewsletterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = ('start_time', 'end_time', 'periodicity', 'status', 'client', 'message',)


class NewsletterManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Newsletter
        fields = ('status',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)