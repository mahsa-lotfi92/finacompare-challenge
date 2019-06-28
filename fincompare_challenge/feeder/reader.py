import csv

from fincompare_challenge.feeder.misc_models import ContactData
from fincompare_challenge.queue.queue import QChannel
import logging

logger = logging.getLogger(__name__)


class Reader:
    def __init__(self, q_name):
        self.q_name = q_name

    def file_to_queue(self, file_address):
        try:
            with open(file=file_address, mode='r') as csv_file:
                with QChannel(self.q_name) as q_channel:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        try:
                            msg = ContactData(name=row[0], email=row[1]).to_json()
                            q_channel.send_message(q_name=self.q_name, message=msg)
                        except Exception as ex:
                            logger.error(ex)

        except FileNotFoundError:
            logger.error(f'The file {file_address} is not found.')
