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
            year=2022,
            week=1,
            region=Region.MAZOWIECKIE,
            deceased_actuals=100
        )

    def test_create_mortality_fact(self):
        """
        MortalityFact object properly created
        """
        self.assertTrue(isinstance(self.mortality_fact, MortalityFact)) 

    def test_dictionaries(self):
        """
        Proper dictionary values set
        """
        self.assertTrue(self.mortality_fact.gender == 0)
        self.assertTrue(self.mortality_fact.age_group == 7)
        self.assertTrue(self.mortality_fact.region == 6)

