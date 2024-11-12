from django.contrib import admin

from newsletter.models import Newsletter


@admin.register(Newsletter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'message', 'periodicity', 'status',)
