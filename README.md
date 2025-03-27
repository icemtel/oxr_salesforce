# Update Salesforce Currencies using Open Exchange Rates API

This package contains a script and a GitHub Action to update currency exchange rates in Salesforce using the Open Exchange Rates API.

The script fetches the latest exchange rates from Open Exchange Rates API and updates both the `CurrencyType` and `DatedConversionRate` objects in Salesforce. 

## Environment Variables

- `OXR_APP_ID`: Open Exchange Rates API key
- `SALESFORCE_EMAIL`: Salesforce username/email
- `SALESFORCE_PASSWORD`:Salesforce password
- `SALESFORCE_TOKEN`: Salesforce security token
- `SALESFORCE_DOMAIN`: Optional: 'test' for a sandbox, or a custom domain.


## Github Actions


## Usage

Example Github workflow that you can add to your repo 

```
name: "Update Currency Exchange Rates"
on:
  workflow_dispatch:

jobs:
  main:
    runs-on: ubuntu-latest

    steps:
    - name: Update Currency Exchange Rates
      uses: icemtel/oxr_salesforce/update_rates_latest@v0.5.0
      with:
        OXR_APP_ID: ${{ secrets.OXR_APP_ID }}
        SALESFORCE_EMAIL: ${{ secrets.SALESFORCE_EMAIL }}
        SALESFORCE_PASSWORD: ${{ secrets.SALESFORCE_PASSWORD }}
        SALESFORCE_TOKEN: ${{ secrets.SALESFORCE_TOKEN }}
        SALESFORCE_DOMAIN: ${{ secrets.SALESFORCE_SANDBOX }}
```