from typing import List

from .mortality_file_extractor import MortalityFileExtractor
from .mortality_xls_extractor import MortalityXLSExtractor


class MortalityActualsExtractor:
    """
    Manages extracting the mortality actuals
    """

    def __init__(self):
        self.files: List[MortalityFileExtractor] = []