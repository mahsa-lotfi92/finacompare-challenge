from fincompare_challenge.consumer.models import Contact
from fincompare_challenge.feeder.misc_models import ContactData
from fincompare_challenge.queue.queue import QChannel


class Consumer:
    @staticmethod
    def callback(ch, method, properties, body):
        obj = ContactData.from_json(data=body)
        Contact.objects.update_or_create(email=obj.email, defaults={'name': obj.name})
        # save the latest name for repeated emails.

    def __init__(self, q_name):
        self.q_name = q_name

    def start_receiving(self):
        QChannel(self.q_name).start_receiving(self.callback)

