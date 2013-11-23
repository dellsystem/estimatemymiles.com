from django.test import TestCase

from howmanymiles.models import Alliance, Airline, FareClass, MileageMultiplier


class AirlineTestCase(TestCase):
    fixtures = ['test/airlines.json']

    def test_get_qualifying_names(self):
        SJ = Airline.objects.get(pk='SJ')
        SJ_miles_name = 'Sleaziness Qualifying Miles (SQM)'
        SJ_segments_name = 'Sleaziness Qualifying Segments (SQS)'
        self.assertEqual(SJ.get_qualifying_miles_name(), SJ_miles_name)
        self.assertEqual(SJ.get_qualifying_segments_name(), SJ_segments_name)


class MileageMultiplierTestCase(TestCase):
    fixtures = ['test/airlines.json', 'test/mileage_multipliers.json']

    def test_get_num_miles(self):
        # Qualifying miles: 25%; regular miles: 50%; minimum miles: 15
        m = MileageMultiplier.objects.get(pk=1)
        normal_miles = m.get_num_miles(100)
        qualifying_miles = m.get_num_miles(100, is_qualifying=True)
        minimum_miles = m.get_num_miles(10)
        minimum_qualifying_miles = m.get_num_miles(10, is_qualifying=True)

        self.assertEqual(normal_miles, 50)
        self.assertEqual(qualifying_miles, 25)
        self.assertEqual(minimum_miles, 15)
        self.assertEqual(minimum_qualifying_miles, 15)
