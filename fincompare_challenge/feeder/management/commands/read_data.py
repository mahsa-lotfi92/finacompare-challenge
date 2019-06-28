import argparse
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from fincompare_challenge.feeder.reader import Reader

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @staticmethod
    def csv_file_name(file_name):
        if len(file_name.split('.')) < 2 or file_name.split('.')[-1] != 'csv':
            raise argparse.ArgumentTypeError('File should be a csv file.')
        return file_name

    def add_arguments(self, parser):
        parser.add_argument('csv_files', nargs='*', type=self.csv_file_name, default=['data_example.csv'])

    def handle(self, *args, **options):
        for file in options['csv_files']:
            # todo: we can get the queue name as an input
            Reader(settings.RABBITMQ_QUEUE_NAME).file_to_queue(file)
            logger.info(f'{file} has been read.')

