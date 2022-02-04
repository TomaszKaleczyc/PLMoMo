from pathlib import Path

from omegaconf import DictConfig

from .mortality_actuals_extractor import MortalityActualsExtractor


class MortalityFactUpdater:
    """
    Manages filling the database
    mortality fact records
    """

    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.mortality_data_path = Path(cfg.mortality_data_path)
        self.mortality_actuals_extractor = MortalityActualsExtractor()

    def update_db(self) -> None:
        """
        Updates the project database mortality facts
        """
        print(self.cfg)
        print(self.mortality_data_path)