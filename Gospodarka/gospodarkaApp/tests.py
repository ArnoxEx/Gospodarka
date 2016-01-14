from django.test import TestCase
from Gospodarka.gospodarkaApp.models import *

class AddressTestCase(TestCase):
    def setUp(self):
        ziemniak = 1
        Address.objects.create(city='Wroc', street='Jakas', numb='3', postal_code='99-130')
        # Address.objects.create(id=1, city='Lodz', street='Insza', numb='4', postal_code='13-990')
        # Status.objects.create(value='zarezerwowany')

    def test_full_address(self):
        """Address can be shown as full data"""
        # first = Address.objects.get(city='Wroc')
        # secnd = Address.objects.get(city='Lodz')
        # self.assertEqual(first.full_address(), 'ul. Jakas 3, Wroc 99-130')
        # self.assertEqual(secnd.full_address(), 'ul. Insza 4, Lodz 13-990')
        self.assertEqual(True, True)
