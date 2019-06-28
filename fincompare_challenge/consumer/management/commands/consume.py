import json
import logging

from fincompare_challenge.consumer.models import Contact
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from fincompare_challenge.queue.queue import QChannel

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        @QChannel.receiver_callback
        def callback(ch, method, properties, body):
            obj = json.loads(body)
            try:
                Contact.objects.update_or_create(email=obj['email'], defaults={'name': obj['name']})
            except IntegrityError as ex:
                pass

        QChannel('emails').receive(callback)

