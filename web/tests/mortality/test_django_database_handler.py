import pandas as pd

from django.test import TransactionTestCase
from model_bakery import baker

from apps.mortality.django_database_handler import DjangoDatabaseHandler
from apps.mortality.models import MortalityFact


class TestDjangoDatabaseHandler(TransactionTestCase):
    """
    DjangoDatabaseHandler tests
    """

    def setUp(self):
        self.database_handler = DjangoDatabaseHandler()
        data_csv_path = 'tests/mortality/test_data/mortality_facts.csv'
        self.mortality_facts = pd.read_csv(data_csv_path, index_col=0)  

    def test_update_actuals(self):
        """
        Database properly updated
        """
        self.database_handler.update_actuals(self.mortality_facts)
        assert len(MortalityFact.objects.all()) == 1216
