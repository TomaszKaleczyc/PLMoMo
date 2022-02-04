from unittest.mock import Mock

from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityXLSXExtractor, MortalityFileExtractor


class TestMortalityXLSExtractor:
    """
    MortalityXLSExtractor tests
    """

    def setup_method(self):
        file_path = Mock()
        self.mortality_xls_extractor = MortalityXLSXExtractor(file_path)

    def test_init(self):
        """
        Object properly instantiated
        """
        assert isinstance(self.mortality_xls_extractor, MortalityFileExtractor)