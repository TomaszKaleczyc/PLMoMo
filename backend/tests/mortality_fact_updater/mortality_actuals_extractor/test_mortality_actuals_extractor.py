from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityActualsExtractor


class TestMortalityActualsExtractor:
    """
    MortalityActualsExtractor tests
    """

    def setup_method(self):
        self.mortality_actuals_extractor = MortalityActualsExtractor()

    def test_init(self):
        """
        Object properly instantiated
        """
        assert self.mortality_actuals_extractor.files == []
