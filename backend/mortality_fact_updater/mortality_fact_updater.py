from .mortality_actuals_extractor import MortalityActualsExtractor


class MortalityFactUpdater:
    """
    Manages filling the database
    mortality fact records
    """

    def __init__(self):
        self.mortality_actuals_extractor = MortalityActualsExtractor()