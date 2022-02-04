from pathlib import PosixPath
from .mortality_file_extractor import MortalityFileExtractor


class MortalityXLSXExtractor(MortalityFileExtractor):
    """
    Extracts mortality facts from Statistics Poland XLS files
    """

    def __init__(self, file_path: PosixPath):
        self.file_path = file_path

    def extract_actuals(self):
        raise NotImplementedError