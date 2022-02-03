from django.db import models


class Gender(models.IntegerChoices):
    """
    Gender dictionary
    """
    MALE = 0, 'Male'
    FEMALE = 1, 'Female'


class AgeGroup(models.IntegerChoices):
    """
    Age group dictionary
    """
    AGE_0_4 = 0, '0 - 4'
    AGE_5_9 = 1, '5 - 9'
    AGE_10_14 = 2, '10 - 14'
    AGE_15_19 = 3, '15 - 19'
    AGE_20_24 = 4, '20 - 24'
    AGE_25_29 = 5, '25 - 29'
    AGE_30_34 = 6, '30 - 34'
    AGE_35_39 = 7, '35 - 39'
    AGE_40_44 = 8, '40 - 44'
    AGE_45_49 = 9, '45 - 49'
    AGE_50_54 = 10, '50 - 54'
    AGE_55_59 = 11, '55 - 59'
    AGE_60_64 = 12, '60 - 64'
    AGE_65_69 = 13, '65 - 69'
    AGE_70_74 = 14, '70 - 74'
    AGE_75_79 = 15, '75 - 79'
    AGE_80_84 = 16, '80 - 84'
    AGE_85_89 = 17, '85 - 89'
    AGE_90_ = 18, '90 +'


class Region(models.IntegerChoices):
    """
    Regions dictionary
    """
    DOLNOSLASKIE = 0, 'Dolnośląskie'
    KUJAWSKO_POMORSKIE = 1, 'Kujawsko-pomorskie'
    LUBELSKIE = 2, 'Lubelskie'
    LUBUSKIE = 3, 'Lubuskie'
    LODZKIE = 4, 'Łódzkie'
    MALOPOLSKIE = 5, 'Małopolskie'
    MAZOWIECKIE = 6, 'Mazowieckie'
    OPOLSKIE = 7, 'Opolskie'
    PODKARPACKIE = 8, 'Podkarpackie'
    PODLASKIE = 9, 'Podlaskie'
    POMORSKIE = 10, 'Pomorskie'
    SLASKIE = 11, 'Śląskie'
    SWIETOKRZYSKIE = 12, 'Świętokrzyskie'
    WARMINSKO_MAZURSKIE = 13, 'Warmińsko-mazurskie'
    WIELKOPOLSKIE = 14, 'Wielkopolskie'
    ZACHODNIOPOMORSKIE = 15, 'Zachodniopomorskie'


class MortalityFact(models.Model):
    """
    ORM representation of the MortalityFact objects
    """
    gender = models.IntegerField(choices=Gender.choices)
    age_group = models.IntegerField(choices=AgeGroup.choices)
    region = models.IntegerField(choices=Region.choices)
    deceased_actuals = models.IntegerField()
    deceased_estimation = models.FloatField(null=True)
    estimation_deviation = models.FloatField(null=True)
