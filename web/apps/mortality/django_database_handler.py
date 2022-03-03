import logging
from omegaconf import DictConfig

from pandas import DataFrame, Series

import django
from django.conf import settings
from web.config import settings as django_settings

if not settings.configured:
    settings.configure(
        DATABASES=django_settings.DATABASES,
        INSTALLED_APPS=[
            'web.apps.mortality',
            ]
    )
    django.setup()
    from .models import MortalityFact
else:
    from apps.mortality.models import MortalityFact

from backend.mortality_fact_updater.database_handler.database_handler import DatabaseHandler



class DjangoDatabaseHandler(DatabaseHandler):
    """
    Handles updating the Django database
    """
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.log = logging.getLogger(__name__)

    def update_actuals(self, mortality_facts: DataFrame) -> None:
        if self.overwrite_completed_years:
            self._remove_historical_years(mortality_facts)
        self.log.info('Writing to django database initiatied...')
        mortality_fact_objects = [
            self._get_fact_object(fact) for _, fact in mortality_facts.iterrows()
            ]
        MortalityFact.objects.bulk_create(mortality_fact_objects)
        self.log.info(f'{len(mortality_fact_objects)} actuals saved to database')

    def _remove_historical_years(self, mortality_facts: DataFrame) -> None:
        """
        Removes existing records for years to be uploaded
        """
        years_to_be_removed = list(mortality_facts.year.unique())
        MortalityFact.objects.filter(year__in=years_to_be_removed).delete()
        self.log.info(f'Historical records removed for years: {years_to_be_removed}')

    def _get_fact_object(self, fact: Series) -> MortalityFact:
        """
        Returns a single fact object
        """
        mortality_fact = MortalityFact(
            gender=fact['gender'],
            age_group=fact['age_group'],
            region=fact['region'],
            year=fact['year'],
            week=fact['week'],
            deceased_actuals=fact['deceased_actuals'],          
        )
        return mortality_fact

    def update_estimations(self) -> None:
        raise NotImplementedError
