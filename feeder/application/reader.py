from queue.queue import QChannel


class Reader:
    def __init__(self, q_name):
        self.q_name = q_name

    def file_to_queue(self, file_address):
        with open(file=file_address, mode='r') as file:
            with QChannel(self.q_name) as q_channel:
                data = file.readlines()
                for d in data:
                    q_channel.send_message(q_name=self.q_name, message=d)

