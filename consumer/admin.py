from django.contrib import admin

from consumer.models import Contact


@admin.register(Contact)
class QuestionTextAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'test']
    search_fields = ['name', 'email']
    readonly_fields = ['email', 'name']
