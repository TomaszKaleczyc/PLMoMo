import logging
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
        self.mortality_actuals_extractor = MortalityActualsExtractor(cfg=cfg)
        self.log = logging.getLogger(__name__)

    def update_db(self) -> None:
        """
        Updates the project database mortality facts
        """
        mortality_facts = self.mortality_actuals_extractor.extract_actuals()
        
