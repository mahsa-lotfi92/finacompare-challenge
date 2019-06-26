import argparse
import logging

from django.core.management.base import BaseCommand

from feeder.reader import Reader

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @staticmethod
    def csv_file_name(file_name):
        if len(file_name.split('.')) < 2 or file_name.split('.')[-1] != 'csv':
            raise argparse.ArgumentTypeError('File should be a csv file.')
        return file_name

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='?', type=self.csv_file_name, default='data_example.csv')

    def handle(self, *args, **options):

        Reader('emails').file_to_queue('data_example.csv')
        logger.info(msg='File has been read.')

