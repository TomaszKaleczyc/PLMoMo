from abc import ABC, abstractmethod
from omegaconf import DictConfig

from pandas import DataFrame


class DatabaseHandler(ABC):
    """
    Abstraction for handling database operations
    in the backend
    """
    cfg: DictConfig

    @property
    def overwrite_completed_years(self) -> bool:
        return self.cfg.db.overwrite_completed_years

    @abstractmethod
    def update_actuals(self, mortality_facts: DataFrame) -> None:
        """
        Updates the mortality actuals in the
        project database
        """

    @abstractmethod
    def update_estimations(self, mortality_estimations: DataFrame) -> None:
        """
        Updates the mortality estimations in the
        project database
        """