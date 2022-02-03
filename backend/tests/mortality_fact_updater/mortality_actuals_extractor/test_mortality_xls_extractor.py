from unittest.mock import Mock

from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityXLSExtractor, MortalityFileExtractor


class TestMortalityXLSExtractor:
    """
    MortalityXLSExtractor tests
    """

    def setup_method(self):
        file_path = Mock()
        self.mortality_xls_extractor = MortalityXLSExtractor(file_path)

    def test_init(self):
        """
        Object properly instantiated
        """
        assert isinstance(self.mortality_xls_extractor, MortalityFileExtractor)