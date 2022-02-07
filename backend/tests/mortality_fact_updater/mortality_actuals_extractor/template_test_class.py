from pathlib import PosixPath
from typing import Dict


class TemplateTestClass:
    """
    Implements common test case functionalities
    """

    tmp_data_dir: PosixPath

    def _create_temporary_files(self, file_counts_by_extension: Dict[str, int]) -> None:
        """
        
        """
        for extension, file_count in file_counts_by_extension.items():
            self._create_temporary_files_with_extension(extension, file_count)
    
    def _create_temporary_files_with_extension(self, extension: str, file_count: int) -> None:
        """
        
        """
        for index in range(file_count):
            file = self.tmp_data_dir.join(f'{index}{extension}')
            file.write(' ')
