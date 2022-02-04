import logging
from pathlib import Path, PosixPath
from typing import List

from omegaconf import DictConfig

from .mortality_file_extractor import MortalityFileExtractor
from .mortality_xlsx_extractor import MortalityXLSXExtractor


class MortalityActualsExtractor:
    """
    Manages extracting the mortality actuals
    """

    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.mortality_data_files: List[MortalityFileExtractor] = []
        self.log = logging.getLogger(__name__)

    def extract_actuals(self) -> None:
        """
        Extracts the mortality data
        """
        self._set_mortality_data_files()

    def _set_mortality_data_files(self) -> None:
        """
        Sets the mortality data files list
        """
        mortality_data_filepaths = self._get_mortality_data_filepaths()
        self.log.info(mortality_data_filepaths)

    def _get_mortality_data_filepaths(self) -> List[PosixPath]:
        """
        Returns paths to mortality data files
        """
        mortality_data_dir = Path(self.cfg.raw_data.mortality_data_dir)
        file_suffix = self.cfg.raw_data.file_suffix
        mortality_data_filepaths = [
            filepath for filepath in mortality_data_dir.iterdir()
            if filepath.suffix == file_suffix
            ]
        return mortality_data_filepaths


