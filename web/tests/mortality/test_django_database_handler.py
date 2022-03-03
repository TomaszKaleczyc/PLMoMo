from unittest.mock import Mock

import pandas as pd
from omegaconf import DictConfig

from django.test import TransactionTestCase
from model_bakery import baker

from apps.mortality.django_database_handler import DjangoDatabaseHandler
from apps.mortality.models import MortalityFact


class TestDjangoDatabaseHandler(TransactionTestCase):
    """
    DjangoDatabaseHandler tests
    """

    def setUp(self):
        self.database_handler = DjangoDatabaseHandler(cfg=Mock())
        data_csv_path = 'tests/mortality/test_data/mortality_facts.csv'
        self.mortality_facts = pd.read_csv(data_csv_path, index_col=0)  

    def test_update_actuals(self):
        """
        Database properly updated
        """
        self.database_handler.update_actuals(self.mortality_facts)
        assert len(MortalityFact.objects.all()) == 1216

    def test_remove_historical_records(self):
        """
        Historical records properly removed
        """
        self._setup_historical_records()
        self.database_handler._remove_historical_years(self.mortality_facts)
        assert len(MortalityFact.objects.all()) == 1

    def test_update_actuals_with_overwriting(self):
        """
        Historical records removed before database update
        """
        self.cfg = DictConfig({
            'db': DictConfig({'overwrite_completed_years': True}),
            })

        self._setup_historical_records()

        self.database_handler.update_actuals(self.mortality_facts)
        assert len(MortalityFact.objects.all()) == 1217

    def _setup_historical_records(self):
        """
        Writes dummy records to the database
        """
        historical_records = [
                MortalityFact(
                    gender=1,
                    age_group=18,
                    region=6,
                    year=2022,
                    week=2,
                    deceased_actuals=164,      
                ),
                MortalityFact(
                    gender=1,
                    age_group=18,
                    region=6,
                    year=2000,
                    week=2,
                    deceased_actuals=164,      
                ),
        ]
        for record in historical_records:
            record.save()


