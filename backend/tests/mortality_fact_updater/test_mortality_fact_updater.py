
from pathlib import PosixPath
import pytest
from unittest.mock import Mock

from omegaconf import DictConfig

from backend.mortality_fact_updater import MortalityFactUpdater
from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityActualsExtractor


def cfg():
    contents = {
        'mortality_data_path': 'test/name'
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
        assert isinstance(self.mortality_fact_updater.mortality_data_path, PosixPath)