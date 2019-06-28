import logging

from fincompare_challenge.consumer.consume import Consumer
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        # todo: we can get the queue name as an input
        Consumer(settings.RABBITMQ_QUEUE_NAME).start_receiving()

