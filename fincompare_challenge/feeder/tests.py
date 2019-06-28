from django.test import TestCase

from fincompare_challenge.feeder.misc_models import ContactData


class ContactDataTest(TestCase):
    def test_email_format(self):
        with self.assertRaises(ValueError):
            ContactData(name='mahsa', email='mahsa.lotfi')
        with self.assertRaises(ValueError):
            ContactData(name='mahsa', email='mahsa')
        with self.assertRaises(ValueError):
            ContactData(name='mahsa', email='mahsa.lotfi@b')
        ContactData(name='mahsa', email='mahsa.lotfi@b.com')
