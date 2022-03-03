import logging
from pathlib import Path

from omegaconf import DictConfig

from .mortality_actuals_extractor import MortalityActualsExtractor
from .database_handler import DatabaseHandler
from web.apps.mortality.django_database_handler import DjangoDatabaseHandler


class MortalityFactUpdater:
    """
    Manages filling the database
    mortality fact records
    """

    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.mortality_actuals_extractor = MortalityActualsExtractor(cfg=cfg)
        self.log = logging.getLogger(__name__)
        self.database_handler: DatabaseHandler = self._get_database_handler()

    @property
    def db_type(self) -> str:
        return self.cfg.db.type

    def _get_database_handler(self) -> DatabaseHandler:
        """
        Returns the proper database handler for the project
        """
        self.log.info(f'Database connection type: {self.db_type}')
        if self.db_type == 'django':
            return DjangoDatabaseHandler(cfg=self.cfg)
        raise NotImplementedError

    def update_db(self) -> None:
        """
        Updates the project database mortality facts
        """
        mortality_facts = self.mortality_actuals_extractor.extract_actuals()
        self.database_handler.update_actuals(mortality_facts)
        self.log.info('Update of mortality facts complete')
        
