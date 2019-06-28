import csv

from fincompare_challenge.feeder.misc_models import ContactData
from fincompare_challenge.queue.queue import QChannel
import logging

logger = logging.getLogger(__name__)


class Reader:
    def __init__(self, q_name):
        self.q_name = q_name

    def send_to_queue(self, csv_reader):
        with QChannel(self.q_name) as q_channel:
            for row in csv_reader:
                try:
                    msg = ContactData(name=row[0], email=row[1]).to_json()
                    q_channel.send_message(q_name=self.q_name, message=msg)
                except Exception as ex:
                    logger.error(ex)

    def read_file(self, file_address):
        try:
            with open(file=file_address, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                self.send_to_queue(csv_reader)

        except FileNotFoundError:
            logger.error(f'The file {file_address} is not found.')
