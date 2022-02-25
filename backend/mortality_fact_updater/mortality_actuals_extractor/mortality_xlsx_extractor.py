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
        gender_sheet_name, gender_id = gender_data
        gender_sheet_facts = self._extract_gender_sheet(gender_sheet_name)
        self.mortality_facts = pd.concat((self.mortality_facts, gender_sheet_facts))

    def _extract_gender_sheet(self, gender_sheet_name: str) -> DataFrame:
        """
        Extracts gender sheet
        """
        raw_annual_gender_mortality_facts = self._read_raw_xlsx_sheet(gender_sheet_name)
        region_gender_mortality_facts = self._map_regions(raw_annual_gender_mortality_facts)
        # self._map_age_groups()
        # 
        return raw_annual_gender_mortality_facts

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

    def _map_regions(self, raw_annual_gender_mortality_facts: DataFrame) -> DataFrame:
        """
        Maps and filters regions
        """
        raw_annual_gender_mortality_facts.rename(columns={'Unnamed: 1': 'region'}, inplace=True)
        region_gender_mortality_facts = raw_annual_gender_mortality_facts[
            raw_annual_gender_mortality_facts['region'].isin(self.regions.keys())
        ].copy()  
        return region_gender_mortality_facts