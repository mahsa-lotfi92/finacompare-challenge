from queue.queue import QChannel
import csv
import json


class Reader:
    def __init__(self, q_name):
        self.q_name = q_name

    def file_to_queue(self, file_address):
        with open(file=file_address, mode='r') as csv_file:
            with QChannel(self.q_name) as q_channel:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    q_channel.send_message(q_name=self.q_name, message=json.dumps({'name': row[0], 'email': row[1]}))
