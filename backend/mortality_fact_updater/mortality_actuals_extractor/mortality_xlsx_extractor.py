
import logging
import re
from copy import copy
from pathlib import PosixPath
from typing import Dict, List, Tuple

import pandas as pd
from pandas import DataFrame, Series
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
    def fact_columns(self) -> List[str]:
        return self.cfg.raw_data.fact_columns

    @property
    def regions(self) -> Dict[str, int]:
        return self.cfg.raw_data.regions

    @property
    def age_groups(self) -> Dict[str, int]:
        return self.cfg.raw_data.age_groups

    @property
    def fact_year(self) -> int:
        return int(self.file_path.stem.split('_')[-1])

    def extract_actuals(self) -> None:
        """
        Extracts mortality data facts
        """
        for gender_data in self.genders.items():
            self._extract_gender_sheet(gender_data)

        if not self.mortality_facts.empty:
            self.log.info(f'Year: {self.fact_year} - {len(self.mortality_facts)} mortality facts extracted ({self.mortality_facts.deceased_actuals.sum():.0f} of deaths in total)')
        
        return self.mortality_facts

    def _extract_gender_sheet(self, gender_data: Tuple[str, int]) -> None:
        """
        Exctracts mortality data facts from a given gender sheet
        """
        gender_sheet = self._get_gender_sheet(gender_data)
        gender_sheet_facts = self._transform_gender_sheet_into_facts_table(gender_sheet)
        self.mortality_facts = pd.concat((self.mortality_facts, gender_sheet_facts))

    def _get_gender_sheet(self, gender_data: Tuple[str, int]) -> DataFrame:
        """
        Extracts gender sheet
        """
        gender_sheet_name, gender_id = gender_data
        raw_annual_gender_mortality_facts = self._read_raw_xlsx_sheet(gender_sheet_name)
        gender_mortality_facts = self._map_gender(raw_annual_gender_mortality_facts, gender_id)
        region_gender_mortality_facts = self._map_regions(gender_mortality_facts)
        gender_sheet = self._map_age_groups(region_gender_mortality_facts)
        return gender_sheet

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
        region_gender_mortality_facts['region'].replace(self.regions, inplace=True)
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
        gender_sheet_facts['age_group'].replace(self.age_groups, inplace=True)
        return gender_sheet_facts

    def _transform_gender_sheet_into_facts_table(self, gender_sheet: DataFrame) -> DataFrame:
        """
        Transforms extracted gender table into facts table
        """
        new_rows = []
        for _, row in gender_sheet.iterrows():
            facts_from_row = self._get_facts_from_row(row)
            new_rows.append(facts_from_row)
        all_facts = sum(new_rows, [])
        gender_sheet_facts = DataFrame(all_facts)
        return gender_sheet_facts

    def _get_facts_from_row(self, row: Series) -> List[dict]:
        """
        Returns all facts from the xls sheet row
        """
        fact_base = self._get_fact_base(row)
        facts_from_row = []
        for column_name in row.index:
            if not self.is_date_column(column_name):
                continue
            fact = self._get_fact(fact_base, column_name, row)
            if pd.isnull(fact['deceased_actuals']):
                continue
            facts_from_row.append(fact)
        return facts_from_row

    def _get_fact_base(self, row: Series) -> dict:
        """
        Returns the fact base for the gender sheet row
        """
        fact_base = {'year': self.reported_year}
        for column_name in row.index:
            if column_name not in self.fact_columns:
                continue
            fact_base[column_name] = row[column_name]
        return fact_base

    def _get_fact(self, fact_base: dict, date_column_name: str, row: Series) -> dict:
        """
        Gets single fact dictionary
        """
        fact = copy(fact_base)
        fact['week'] = self._get_week_number(date_column_name)
        fact['deceased_actuals'] = row[date_column_name]
        return fact

    @staticmethod
    def _get_week_number(date_column_name: str):
        """
        Returns the week number from the column name
        """
        return int(date_column_name[1:])
    
    @staticmethod
    def is_date_column(column_name: str) -> bool:
        """
        Checks if column name refers to a date column
        """
        match = re.match('^[T][0-9][0-9]', column_name)
        return match is not None
