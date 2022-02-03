<img src="web/static/images/logo.png" alt="drawing" width="400"/>

#  Polish Mortality Monitoring system

This project is intended to create a website allowing interactive deepdive into mortality data for Poland, aiming to detect and measure excess deaths related to seasonal influenza, pandemics and other public health threats. It is to be based on the functionalities and information hosted by the [EuroMOMO](https://www.euromomo.eu/). 

As of January 2022, Poland is still not part of the EuroMOMO project, which has been a major motivation to start this project, with the aid of data distributed by the Statistics Poland bureau (aka [GUS](https://stat.gov.pl/)).

## Resources

* Dataset: [Statistics Poland mortality data](https://stat.gov.pl/obszary-tematyczne/ludnosc/ludnosc/zgony-wedlug-tygodni,39,2.html)
* Working environment: Ubuntu18.04 LTS / Python 3.6.9 / virtualenv / Docker version 20.10.6

## Project structure

```
├── backend                             # Application backend code
│   └── tests                           # Backend code tests
├── data                                # Data used in the project
│   └── mortality                       # Spreadsheets with mortality data sourced from Statistics Poland
├── docs                                # Additional process documentation
├── environment                         # Definition and contents of the project environment
└── web                                 # Web application code

```

## Acknowledgements

* Special thanks to [Łukasz Popardowski](http://popardowski.pl/web/) - the author of [the code behind the interactive map of Poland](https://cssmapsplugin.com/get/poland/)