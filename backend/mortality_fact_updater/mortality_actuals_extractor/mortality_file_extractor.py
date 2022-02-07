from abc import ABC, abstractmethod
from pathlib import PosixPath

from omegaconf import DictConfig


class MortalityFileExtractor(ABC):
    """
    Mortality file extraction abstract class
    """
    file_path: PosixPath
    cfg: DictConfig

    @abstractmethod
    def extract_actuals(self):
        """
        Extracts mortality data from file
        """