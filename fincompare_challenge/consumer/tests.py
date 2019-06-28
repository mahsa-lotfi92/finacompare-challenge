from unittest.mock import patch, MagicMock

from django.test import TestCase

from fincompare_challenge.consumer.consume import Consumer
from fincompare_challenge.consumer.models import Contact
from fincompare_challenge.feeder.misc_models import ContactData


class ConsumerTest(TestCase):
    @patch('fincompare_challenge.queue.queue.QChannel.start_receiving', new_callable=MagicMock)
    def test_start_receiving(self, queue_start_receiving_mock):
        uut = Consumer('emails')
        cd1 = ContactData(name='Mahsa Lotfi', email='mahsa.lotfi92@gmail.com')
        cd2 = ContactData(name='Mahsa Lotfi', email='mahsa.lotfi92@yahoo.com')

        def queue_start_receiving(callback):
            callback(ch=None, properties=None, method=None, body=cd1.to_json())
            callback(ch=None, properties=None, method=None, body=cd2.to_json())

        queue_start_receiving_mock.side_effect = queue_start_receiving

        uut.start_receiving()
        self.assertEqual(Contact.objects.count(), 2)

    @patch('fincompare_challenge.queue.queue.QChannel.start_receiving', new_callable=MagicMock)
    def test_no_email_duplication(self, queue_start_receiving_mock):
        uut = Consumer('emails')
        cd1 = ContactData(name='Mahsa Lotfi', email='mahsa.lotfi92@gmail.com')
        cd2 = ContactData(name='Mahsa L', email='mahsa.lotfi92@gmail.com')

        def queue_start_receiving(callback):
            callback(ch=None, properties=None, method=None, body=cd1.to_json())
            callback(ch=None, properties=None, method=None, body=cd2.to_json())

        queue_start_receiving_mock.side_effect = queue_start_receiving

        uut.start_receiving()
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.last().name, 'Mahsa L')



