import logging
from pathlib import PosixPath
from typing import Dict, Optional, Tuple

import pandas as pd
from pandas import DataFrame
from omegaconf import DictConfig

from .mortality_file_extractor import MortalityFileExtractor


class MortalityXLSXExtractor(MortalityFileExtractor):
    """
    Extracts mortality facts from Statistics Poland XLS files
    """

    def __init__(self, file_path: PosixPath, cfg: DictConfig):
        self.file_path = file_path
        self.cfg = cfg
        self.mortality_facts = DataFrame()
        self.log = logging.getLogger(__name__)
    
    @property
    def reported_year(self) -> int:
        """
        Returns the reported actuals year
        """
        return int(self.file_path.stem.split('_')[-1])

    @property
    def genders(self) -> Dict[str, int]:
        return self.cfg.raw_data.genders

    @property
    def regions(self) -> Dict[str, int]:
        return self.cfg.raw_data.regions

    @property
    def age_groups(self) -> Dict[str, int]:
        return self.cfg.raw_data.age_groups

    def extract_actuals(self) -> None:
        """
        Extracts mortality data facts
        """
        for gender_data in self.genders.items():
            self._extract_gender_sheet(gender_data)

    def _extract_gender_sheet(self, gender_data: Tuple[str, int]) -> None:
        """
        Exctracts mortality data facts from a given gender sheet
        """
        gender_sheet_facts = self._get_gender_sheet(gender_data)
        self.mortality_facts = pd.concat((self.mortality_facts, gender_sheet_facts))

    def _get_gender_sheet(self, gender_data: Tuple[str, int]) -> DataFrame:
        """
        Extracts gender sheet
        """
        gender_sheet_name, gender_id = gender_data
        raw_annual_gender_mortality_facts = self._read_raw_xlsx_sheet(gender_sheet_name)
        gender_mortality_facts = self._map_gender(raw_annual_gender_mortality_facts, gender_id)
        region_gender_mortality_facts = self._map_regions(gender_mortality_facts)
        gender_sheet_facts = self._map_age_groups(region_gender_mortality_facts)
        return gender_sheet_facts

    def _read_raw_xlsx_sheet(self, gender_sheet_name: str) -> DataFrame:
        """
        Reads a raw xlsx sheet
        """
        raw_annual_mortality_facts = pd.read_excel(self.file_path, 
                        engine='openpyxl',
                        header=6,
                        sheet_name=gender_sheet_name)
        raw_annual_mortality_facts = raw_annual_mortality_facts[1:]  # first row is blank, skipping row in pandas doesn't work correctly
        return raw_annual_mortality_facts

    def _map_gender(self, raw_annual_gender_mortality_facts: DataFrame, gender_id: int) -> DataFrame:
        """
        Maps gender
        """
        gender_mortality_facts = raw_annual_gender_mortality_facts.copy()
        gender_mortality_facts['gender'] = gender_id
        return gender_mortality_facts

    def _map_regions(self, raw_annual_gender_mortality_facts: DataFrame) -> DataFrame:
        """
        Maps and filters regions
        """
        region_column = raw_annual_gender_mortality_facts.columns[1]
        raw_annual_gender_mortality_facts.rename(columns={region_column: 'region'}, inplace=True)
        region_gender_mortality_facts = raw_annual_gender_mortality_facts[
            raw_annual_gender_mortality_facts['region'].isin(self.regions.keys())
        ].copy()
        return region_gender_mortality_facts

    def _map_age_groups(self, region_gender_mortality_facts: DataFrame) -> DataFrame:
        """
        Maps and filters age groups
        """
        age_group_column = region_gender_mortality_facts.columns[0]
        region_gender_mortality_facts.rename(columns={age_group_column: 'age_group'}, inplace=True)
        gender_sheet_facts = region_gender_mortality_facts[
            region_gender_mortality_facts['age_group'].isin(self.age_groups.keys())
        ].copy()
        return gender_sheet_facts