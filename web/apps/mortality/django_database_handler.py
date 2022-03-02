import logging

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
    def __init__(self):
        self.log = logging.getLogger(__name__)

    def update_actuals(self, mortality_facts: DataFrame) -> None:
        self.log.info('Writing to django database initiatied...')
        mortality_fact_objects = [
            self._get_fact_object(fact) for _, fact in mortality_facts.iterrows()
            ]
        MortalityFact.objects.bulk_create(mortality_fact_objects)
        self.log.info(f'{len(mortality_fact_objects)} actuals saved to database')

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
