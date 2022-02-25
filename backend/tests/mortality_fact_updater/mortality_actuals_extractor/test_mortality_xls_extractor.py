import pytest
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
from omegaconf.dictconfig import DictConfig

from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityXLSXExtractor, MortalityFileExtractor


def cfg():
    return DictConfig({
        'raw_data': DictConfig(
            {'genders': {'MĘŻCZYŹNI': 0, 'KOBIETY': 1}}
        )
    })


@pytest.fixture
def raw_annual_mortality_df():
    data_csv_path = 'backend/tests/mortality_fact_updater/mortality_actuals_extractor/test_data/raw_annual_mortality_df.csv'
    return pd.read_csv(data_csv_path, index_col=0)


class TestMortalityXLSExtractor:
    """
    MortalityXLSExtractor tests
    """

    def setup_method(self):
        file_path = Path('backend/tests/mortality_fact_updater/mortality_actuals_extractor/test_data/Zgony według tygodni w Polsce_2022.xlsx')
        self.mortality_xls_extractor = MortalityXLSXExtractor(file_path, cfg())

    def test_init(self):
        """
        Object properly instantiated
        """
        assert isinstance(self.mortality_xls_extractor, MortalityFileExtractor)
        assert isinstance(self.mortality_xls_extractor.cfg, DictConfig)

    @pytest.mark.parametrize('gender_sheet_name, expected_deceased_sum', [
        ('MĘŻCZYŹNI', 10448),
        ('KOBIETY', 10604)
    ])
    def test_extract_gender_sheet(self, gender_sheet_name, expected_deceased_sum):
        """
        Gender sheet properly extracted
        """
        mortality_gender_facts = self.mortality_xls_extractor._extract_gender_sheet(gender_sheet_name)
        assert not mortality_gender_facts.empty
        # assert mortality_gender_facts['deceased_actuals'].sum() == expected_deceased_sum

    @pytest.mark.parametrize('gender_sheet_name, expected_deceased_w2_sum', [
        ('MĘŻCZYŹNI', 38328),
        ('KOBIETY', 39536)
    ])
    def test_read_raw_xlsx_sheet(self, gender_sheet_name, expected_deceased_w2_sum):
        """
        Gender sheet properly extracted
        """
        raw_annual_mortality_facts = self.mortality_xls_extractor._extract_gender_sheet(gender_sheet_name)
        assert raw_annual_mortality_facts['T02'].sum() == expected_deceased_w2_sum