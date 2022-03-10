<img src="web/static/images/logo.png" alt="drawing" width="435"/>

#  Polish Mortality Monitoring System

This project is intended to create a website allowing interactive deepdive into mortality data for Poland, aiming to detect and measure excess deaths related to seasonal influenza, pandemics and other public health threats. It is to be based on the functionalities and information hosted by the [EuroMOMO](https://www.euromomo.eu/). 

As of January 2022, Poland is still not part of the EuroMOMO project, which has been a major motivation to start this project, with the aid of data distributed by the Statistics Poland bureau (aka [GUS](https://stat.gov.pl/)).

## Resources

* Dataset: [Statistics Poland mortality data](https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/zgony-wedlug-tygodni,39,2.html)
* Working environment: Ubuntu18.04 LTS / Python 3.6.9 / virtualenv / Docker version 20.10.6

## Project structure

```
├── backend                             # Application backend code (see: backend/README.md)
├── data                                # Data used in the project
│   └── mortality                       # Spreadsheets with mortality data sourced from Statistics Poland
├── docs                                # Additional process documentation
├── environment                         # Definition and contents of the project environment
└── web                                 # Web application code

```

## Working with the project

Before launching the project, define your `.env` file in the project root directory. You will find the `.env.example` file with default settings.

From the root of the project repository, use the included Makefile to:

* build the app containers - `make docker-build`
* launch the app containers - `make docker-up`. The web app will become available on the port defined in the `.env` file)
* stop the app containers - `make docker-down`


## Acknowledgements

* Special thanks to [Łukasz Popardowski](http://popardowski.pl/web/) - the author of [the code behind the interactive map of Poland](https://cssmapsplugin.com/get/poland/)