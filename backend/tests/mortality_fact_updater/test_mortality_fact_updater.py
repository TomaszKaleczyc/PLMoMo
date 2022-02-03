from unittest.mock import Mock

from backend.mortality_fact_updater import MortalityFactUpdater
from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityActualsExtractor


class TestMortalityFactUpdater:
    """
    MortalityFactUpdater tests
    """

    def setup_method(self):
        self.mortality_fact_updater = MortalityFactUpdater()

    def test_init(self):
        """
        Object properly instantiated
        """
        assert isinstance(self.mortality_fact_updater.mortality_actuals_extractor, MortalityActualsExtractor)