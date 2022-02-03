# PLMoMo backend

This component is responsible for updating the project database.

```
├── config                                  # Backend configuration                      # 
├── mortality_fact_updater                  # Responsible for filling the database mortality fact table          
│   ├── mortality_actuals_extractor         # Responsible for extracting the mortality actuals
│   └── mortality_baseline_estimator        # Responsible for estimating the mortality baseline values
├── tests                                   # Code unit and functional tests
└── utilities                               # Utility functions and classes
```