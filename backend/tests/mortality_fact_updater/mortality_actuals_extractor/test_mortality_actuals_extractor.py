import pytest

from omegaconf import DictConfig

from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityActualsExtractor, MortalityXLSXExtractor
from .template_test_class import TemplateTestClass

def cfg():
    contents = {
        'raw_data': DictConfig({
            'mortality_data_dir': None,
            'file_suffix': None,
        })
    }
    return DictConfig(contents)
    

class TestMortalityActualsExtractor(TemplateTestClass):
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


    @pytest.mark.parametrize('mortality_file_suffix, expected_num_files',[
        ('.xlsx', 5),
    ])
    def test_get_mortality_data_filepaths(self, tmpdir, mortality_file_suffix, expected_num_files):
        """
        Mortality file paths identified correctly
        """
        self.tmp_data_dir = tmpdir.mkdir('tmpdata')
        file_counts_by_extension = {
            '.xlsx': 5,
            '.xls': 2,
            '.pdf': 10,
        }
        self._create_temporary_files(file_counts_by_extension)
        self.mortality_actuals_extractor.cfg.raw_data.mortality_data_dir = str(self.tmp_data_dir)
        self.mortality_actuals_extractor.cfg.raw_data.file_suffix = mortality_file_suffix
        mortality_data_filepaths = self.mortality_actuals_extractor._get_mortality_data_filepaths()
        assert(len(mortality_data_filepaths) == expected_num_files)

    @pytest.mark.parametrize('mortality_file_suffix, expected_output', [
        ('.xlsx', MortalityXLSXExtractor),
        ('.foo', None),
    ])
    def test_get_mortality_file_extractor(self, mortality_file_suffix, expected_output):
        """
        Proper mortality file extractor returned
        """
        self.mortality_actuals_extractor.cfg.raw_data.file_suffix = mortality_file_suffix
        if expected_output is None:
            with pytest.raises(NotImplementedError) as error:
                mortality_file_extractor = self.mortality_actuals_extractor._get_mortality_file_extractor()
        else:
            mortality_file_extractor = self.mortality_actuals_extractor._get_mortality_file_extractor()
            assert mortality_file_extractor == expected_output
