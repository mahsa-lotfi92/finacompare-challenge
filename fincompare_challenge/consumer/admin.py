from fincompare_challenge.consumer.models import Contact
from django.contrib import admin


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'name']
    search_fields = ['name', 'email']
    readonly_fields = ['email', 'name']
