from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from negotiators.models import Negotiator


class AgreementCalendarTest(APITestCase):
    fixtures = ['general/fixtures/countries.json', 'general/fixtures/negotiators.json', 'general/fixtures/general.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = Negotiator.objects.create(email='admin@test.com', is_staff=True)
        cls.view_name = 'agreement_calendar'

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_agreement_calendar(self):
        response = self.client.get(reverse(self.view_name))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['2018'][2], 1)
        self.assertEqual(response.json()['2018'][6], 2)
        self.assertEqual(response.json()['2019'][5], 2)

    def test_agreement_calendar_with_get_parameters_country_negotiator(self):
        response = self.client.get(f'{reverse(self.view_name)}?country=1,43&negotiator=1,2,5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['2018'][2], 1)
        self.assertFalse(response.json().get('2019'))

    def test_agreement_calendar_with_get_parameters_country_company(self):
        response = self.client.get(f'{reverse(self.view_name)}?company=2,5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['2018'][6], 1)
        self.assertFalse(response.json().get('2019'))
