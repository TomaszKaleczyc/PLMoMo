from abc import ABC, abstractmethod
from pathlib import PosixPath


class MortalityFileExtractor(ABC):
    """
    Mortality file extraction abstract class
    """
    file_path: PosixPath

    @abstractmethod
    def extract_actuals(self):
        """
        Extracts mortality data from file
        """