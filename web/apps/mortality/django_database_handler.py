from pandas import DataFrame

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

    def update_actuals(self, mortality_facts: DataFrame) -> None:
        for _, fact in mortality_facts.iterrows():
            mortality_fact = MortalityFact(
                gender=fact['gender'],
                age_group=fact['age_group'],
                region=fact['region'],
                year=fact['year'],
                week=fact['week'],
                deceased_actuals=fact['deceased_actuals'],          
            )
            mortality_fact.save()

    def update_estimations(self) -> None:
        raise NotImplementedError