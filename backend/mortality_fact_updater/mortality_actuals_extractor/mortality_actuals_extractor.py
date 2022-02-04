import logging
from pathlib import Path
from typing import List

from omegaconf import DictConfig

from .mortality_file_extractor import MortalityFileExtractor
from .mortality_xls_extractor import MortalityXLSExtractor


class MortalityActualsExtractor:
    """
    Manages extracting the mortality actuals
    """

    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.mortality_data_path = Path(cfg.mortality_data_path)
        self.mortality_data_files: List[MortalityFileExtractor] = []
        self.log = logging.getLogger(__name__)

    def extract_actuals(self):
        """
        Extracts the mortality data
        """
        self._set_mortality_data_files()

    def _set_mortality_data_files(self) -> None:
        """
        Sets the mortality data files list
        """
