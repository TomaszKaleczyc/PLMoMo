from django.test import TransactionTestCase
from model_bakery import baker

from apps.mortality.models import MortalityFact, AgeGroup, Gender, Region


class MortalityFactTestModel(TransactionTestCase):
    """
    MortalityFact tests
    """

    def setUp(self):
        self.mortality_fact = baker.make(
            'MortalityFact',
            gender=Gender.MALE,
            age_group=AgeGroup.AGE_35_39,
            region=Region.MAZOWIECKIE,
            deceased_actuals=100
        )

    def test_create_mortality_fact(self):
        """
        MortalityFact object properly created
        """
        self.assertTrue(isinstance(self.mortality_fact, MortalityFact))

