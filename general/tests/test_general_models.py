from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from general.models import Period, Company, Country, Status, Agreement
from negotiators.models import Negotiator


class GeneralModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.negotiator = Negotiator.objects.create(email='test@email.com')
        cls.country = Country.objects.create(name='Test', code='TST')
        cls.company = Company.objects.create(
            country=cls.country,
            title='Test'
        )
        cls.status = Status.objects.create(name="status")
        cls.agreement = Agreement.objects.create(
            start_date=timezone.now() - timedelta(days=20),
            stop_date=timezone.now() + timedelta(days=20),
            company=cls.company,
            negotiator=cls.negotiator
        )

    def test_period_creation_start_later_stop_date(self):
        with self.assertRaises(ValueError) as e:
            Period.objects.create(
                start_date=timezone.now() + timedelta(days=2),
                stop_date=timezone.now(),
                status=self.status,
                agreement=self.agreement
            )
        self.assertEqual(str(e.exception), 'Period start date could NOT be later than stop date')

    def test_period_creation_start_earlier_start_agreement_date(self):
        with self.assertRaises(ValueError) as e:
            Period.objects.create(
                start_date=timezone.now() - timedelta(days=30),
                stop_date=timezone.now(),
                status=self.status,
                agreement=self.agreement
            )
        self.assertEqual(str(e.exception),
                         'Agreement start date could NOT be earlier than start date of the earliest period')

    def test_period_creation_stop_later_stop_agreement_date(self):
        with self.assertRaises(ValueError) as e:
            Period.objects.create(
                start_date=timezone.now(),
                stop_date=timezone.now() + timedelta(days=30),
                status=self.status,
                agreement=self.agreement
            )
        self.assertEqual(str(e.exception),
                         'Agreement stop date could NOT be later than stop date of the latest period')

    def test_intersected_periods(self):
        with self.assertRaises(ValueError) as e:
            Period.objects.create(
                start_date=timezone.now(),
                stop_date=timezone.now() + timedelta(days=2),
                status=self.status,
                agreement=self.agreement
            )
            Period.objects.create(
                start_date=timezone.now() + timedelta(days=1),
                stop_date=timezone.now() + timedelta(days=4),
                status=self.status,
                agreement=self.agreement
            )
        self.assertEqual(str(e.exception), 'Inside agreement periods should not intersect')

    def test_intersected_periods_one_inside_another(self):
        with self.assertRaises(ValueError) as e:
            Period.objects.create(
                start_date=timezone.now(),
                stop_date=timezone.now() + timedelta(days=9),
                status=self.status,
                agreement=self.agreement
            )
            Period.objects.create(
                start_date=timezone.now() + timedelta(days=1),
                stop_date=timezone.now() + timedelta(days=4),
                status=self.status,
                agreement=self.agreement
            )
        self.assertEqual(str(e.exception), 'Inside agreement periods should not intersect')


    def test_agreement_creation_start_later_stop_date(self):
        with self.assertRaises(ValueError) as e:
            Agreement.objects.create(
                start_date=timezone.now() + timedelta(days=2),
                stop_date=timezone.now(),
                company=self.company,
                negotiator=self.negotiator
            )
        self.assertEqual(str(e.exception), 'Agreement start date could NOT be later than stop date')
