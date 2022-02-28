
from pathlib import PosixPath
import pytest
from unittest.mock import Mock

from omegaconf import DictConfig

from backend.mortality_fact_updater.database_handler import DatabaseHandler
from backend.mortality_fact_updater import MortalityFactUpdater
from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityActualsExtractor
from web.apps.mortality.django_database_handler import DjangoDatabaseHandler


def cfg():
    contents = {
        'mortality_data_path': 'test/name',
        'db': DictConfig({'type': 'django'}),
    }
    return DictConfig(contents)
    

class TestMortalityFactUpdater:
    """
    MortalityFactUpdater tests
    """

    def setup_method(self):
        self.mortality_fact_updater = MortalityFactUpdater(cfg())

    def test_init(self):
        """
        Object properly instantiated
        """
        assert isinstance(self.mortality_fact_updater.mortality_actuals_extractor, MortalityActualsExtractor)
        assert isinstance(self.mortality_fact_updater.database_handler, DatabaseHandler)

    def test_get_database_handler(self):
        """
        Proper database handler returned
        """
        assert isinstance(self.mortality_fact_updater._get_database_handler(), DjangoDatabaseHandler)
        self.mortality_fact_updater.cfg['db'] = DictConfig({'type': 'test'})
        with pytest.raises(NotImplementedError):
            self.mortality_fact_updater._get_database_handler()