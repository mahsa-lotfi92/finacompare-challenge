from django.contrib import admin

from consumer.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'name']
    search_fields = ['name', 'email']
    readonly_fields = ['email', 'name']
