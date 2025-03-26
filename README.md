# Update Salesforce Currencies using Open Exchange Rates API

This package contains a script and a GitHub Action to update currency exchange rates in Salesforce using the Open Exchange Rates API.

The script fetches the latest exchange rates from Open Exchange Rates API and updates both the `CurrencyType` and `DatedConversionRate` objects in Salesforce. 

## Environment Variables

- `OXR_APP_ID`: Open Exchange Rates API key
- `SALESFORCE_EMAIL`: Salesforce email
- `SALESFORCE_PASSWORD`:Salesforce password
- `SALESFORCE_TOKEN`: Salesforce security token
- `SALESFORCE_SANDBOX`: Sandbox name, optional.

## Usage

After installing the dependencies and populating env variables, either run the script manually

```
python update_exchange_rates.py
```

or use the Github Action.


## TODOs

- support updating multiple currencies in an efficient manner 
- make it easy to set the list of currencies & schedule