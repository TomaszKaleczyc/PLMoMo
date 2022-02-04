from pathlib import PosixPath
from omegaconf import DictConfig

from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityActualsExtractor

def cfg():
    contents = {
        'mortality_data_path': 'test/name'
    }
    return DictConfig(contents)
    

class TestMortalityActualsExtractor:
    """
    MortalityActualsExtractor tests
    """

    def setup_method(self):
        self.mortality_actuals_extractor = MortalityActualsExtractor(cfg())

    def test_init(self):
        """
        Object properly instantiated
        """
        assert isinstance(self.mortality_actuals_extractor.cfg, DictConfig)
        assert self.mortality_actuals_extractor.mortality_data_files == []

    # def test_set_mortality_files(self):
    #     """
    #     Mortality file
    #     """
