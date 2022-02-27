from abc import ABC, abstractmethod
from pathlib import PosixPath

from pandas import DataFrame
from omegaconf import DictConfig


class MortalityFileExtractor(ABC):
    """
    Mortality file extraction abstract class
    """
    file_path: PosixPath
    cfg: DictConfig

    @abstractmethod
    def extract_actuals(self) -> DataFrame:
        """
        Extracts mortality data from file into a DataFrame
        """