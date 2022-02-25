import pytest
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
from omegaconf.dictconfig import DictConfig

from backend.mortality_fact_updater.mortality_actuals_extractor import MortalityXLSXExtractor, MortalityFileExtractor


def cfg():
    return DictConfig({
        'raw_data': DictConfig(
            {
                'genders': {'MĘŻCZYŹNI': 0, 'KOBIETY': 1},
                'regions': {
                    "PL51": 0,  # Dolnośląskie
                    "PL61": 1,  # Kujawsko-pomorskie
                    "PL81": 2,  # Lubelskie
                    "PL43": 3,  # Lubuskie
                    "PL71": 4,  # Łódzkie
                    "PL21": 5,  # Małopolskie
                    "PL9": 6,   # Mazowieckie - macroregion!
                    "PL52": 7,  # Opolskie
                    "PL82": 8,  # Podkarpackie
                    "PL84": 9,  # Podlaskie
                    "PL63": 10, # Pomorskie
                    "PL22": 11, # Śląskie
                    "PL72": 12, # Świętokrzyskie
                    "PL62": 13, # Warmińsko-mazurskie
                    "PL41": 14, # Wielkopolskie
                    "PL42": 15  # Zachodniopomorskie
                    },
                'age_groups': {
                    "0 - 4": 0,
                    "5 - 9": 1,
                    "10 - 14": 2,
                    "15 - 19": 3,
                    "20 - 24": 4,
                    "25 - 29": 5,
                    "30 - 34": 6,
                    "35 - 39": 7,
                    "40 - 44": 8,
                    "45 - 49": 9,
                    "50 - 54": 10,
                    "55 - 59": 11,
                    "60 - 64": 12,
                    "65 - 69": 13,
                    "70 - 74": 14,
                    "75 - 79": 15,
                    "80 - 84": 16,
                    "85 - 89": 17,
                    "90 i więcej": 18
                    }
                }
        )
    })


@pytest.fixture
def raw_annual_gender_mortality_facts():
    data_csv_path = 'backend/tests/mortality_fact_updater/mortality_actuals_extractor/test_data/raw_annual_mortality_df.csv'
    return pd.read_csv(data_csv_path, index_col=0)


@pytest.fixture
def gender_sheet():
    data_csv_path = 'backend/tests/mortality_fact_updater/mortality_actuals_extractor/test_data/gender_sheet.csv'
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

    @pytest.mark.parametrize('gender_data, expected_deceased_w1_sum', [
        (('MĘŻCZYŹNI', 0), 5657),
        (('KOBIETY', 1), 5662)
    ])
    def test_get_gender_sheet(self, gender_data, expected_deceased_w1_sum):
        """
        Gender sheet properly extracted
        """
        gender_sheet = self.mortality_xls_extractor._get_gender_sheet(gender_data)
        assert gender_sheet['T01'].sum() == expected_deceased_w1_sum
        for column in ['gender', 'age_group', 'region']:
            assert column in gender_sheet.columns

    @pytest.mark.parametrize('gender_sheet_name, expected_deceased_w2_sum', [
        ('MĘŻCZYŹNI', 38328),
        ('KOBIETY', 39536)
    ])
    def test_read_raw_xlsx_sheet(self, gender_sheet_name, expected_deceased_w2_sum):
        """
        Gender sheet properly extracted
        """
        raw_annual_gender_mortality_facts = self.mortality_xls_extractor._read_raw_xlsx_sheet(gender_sheet_name)
        assert raw_annual_gender_mortality_facts['T02'].sum() == expected_deceased_w2_sum

    def test_map_gender(self, raw_annual_gender_mortality_facts):
        """
        Gender data properly mapped
        """
        gender_id = 1
        gender_mortality_facts = self.mortality_xls_extractor._map_gender(raw_annual_gender_mortality_facts, gender_id)
        assert 'gender' in gender_mortality_facts.columns
        assert gender_mortality_facts['gender'].max() == gender_id

    def test_map_regions(self, raw_annual_gender_mortality_facts):
        """
        Region information properly mapped
        """
        region_gender_mortality_facts = self.mortality_xls_extractor._map_regions(raw_annual_gender_mortality_facts)
        assert region_gender_mortality_facts['T01'].sum() == 11324
        assert 'region' in region_gender_mortality_facts.columns
        assert region_gender_mortality_facts['region'].max() == 15

    def test_map_age_groups(self, raw_annual_gender_mortality_facts):
        """
        Age group information properly mapped
        """
        gender_sheet = self.mortality_xls_extractor._map_age_groups(raw_annual_gender_mortality_facts)
        assert gender_sheet['T01'].sum() == 22648
        assert 'age_group' in gender_sheet.columns
        assert gender_sheet['age_group'].max() == 18

    def test_transform_gender_sheet_into_facts_table(self, gender_sheet):
        """
        Extracted gender sheet properly transformed into fact table
        """
        gender_sheet_facts = self.mortality_xls_extractor._transform_gender_sheet_into_facts_table(gender_sheet)

