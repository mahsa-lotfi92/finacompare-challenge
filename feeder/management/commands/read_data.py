import logging

from django.core.management.base import BaseCommand

from feeder.reader import Reader

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Reader('emails').file_to_queue('data_example.csv')
        logger.info(msg='File has been read.')

