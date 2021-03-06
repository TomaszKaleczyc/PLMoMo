# Generated by Django 3.1 on 2022-02-28 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MortalityFact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(0, 'Male'), (1, 'Female')])),
                ('age_group', models.IntegerField(choices=[(0, '0 - 4'), (1, '5 - 9'), (2, '10 - 14'), (3, '15 - 19'), (4, '20 - 24'), (5, '25 - 29'), (6, '30 - 34'), (7, '35 - 39'), (8, '40 - 44'), (9, '45 - 49'), (10, '50 - 54'), (11, '55 - 59'), (12, '60 - 64'), (13, '65 - 69'), (14, '70 - 74'), (15, '75 - 79'), (16, '80 - 84'), (17, '85 - 89'), (18, '90 +')])),
                ('region', models.IntegerField(choices=[(0, 'Dolnośląskie'), (1, 'Kujawsko-pomorskie'), (2, 'Lubelskie'), (3, 'Lubuskie'), (4, 'Łódzkie'), (5, 'Małopolskie'), (6, 'Mazowieckie'), (7, 'Opolskie'), (8, 'Podkarpackie'), (9, 'Podlaskie'), (10, 'Pomorskie'), (11, 'Śląskie'), (12, 'Świętokrzyskie'), (13, 'Warmińsko-mazurskie'), (14, 'Wielkopolskie'), (15, 'Zachodniopomorskie')])),
                ('year', models.IntegerField()),
                ('week', models.IntegerField()),
                ('deceased_actuals', models.IntegerField()),
            ],
        ),
    ]
