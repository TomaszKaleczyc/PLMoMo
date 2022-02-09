import logging
from pathlib import PosixPath
from typing import Dict, Tuple

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
        mortality_gender_facts = self._extract_gender_sheet(gender_sheet_name)

    def _extract_gender_sheet(self, gender_sheet_name: str) -> DataFrame:
        """
        Extracts gender sheet
        """
        raw_annual_mortality_df = pd.read_excel(self.file_path, 
                        engine='openpyxl',
                        header=6,
                        sheet_name=gender_sheet_name)
        raw_annual_mortality_df = raw_annual_mortality_df[1:]  # first row is blank, skipping row in pandas doesn't work correctly
        return raw_annual_mortality_df
