from pandas import DataFrame

from backend.mortality_fact_updater.database_handler.database_handler import DatabaseHandler
# from .models import MortalityFact


class DjangoDatabaseHandler(DatabaseHandler):
    """
    Handles updating the Django database
    """

    def update_actuals(self, mortality_facts: DataFrame) -> None:

        ...

    def update_estimations(self) -> None:
        raise NotImplementedError