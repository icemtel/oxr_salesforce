# Update Salesforce Currency form GitHub Actions

This package contains a python script and a reusable GitHub Action to update currency exchange rates in Salesforce using the Open Exchange Rates API.

## Github Actions

## Usage

```
jobs:
  job_id:
    runs-on: ubuntu-latest

    steps:
    - uses: icemtel/oxr_salesforce/update_rates_latest@<VERSION_TAG> # replace with the most recent version!
      with:
        OXR_APP_ID: ${{ secrets.OXR_APP_ID }}
        SALESFORCE_EMAIL: ${{ secrets.SALESFORCE_EMAIL }}
        SALESFORCE_PASSWORD: ${{ secrets.SALESFORCE_PASSWORD }}
        SALESFORCE_TOKEN: ${{ secrets.SALESFORCE_TOKEN }}
        SALESFORCE_DOMAIN: ${{ secrets.SALESFORCE_DOMAIN }}
```


### Environment Variables

- `OXR_APP_ID`: Open Exchange Rates API key
- `SALESFORCE_EMAIL`: Salesforce username/email
- `SALESFORCE_PASSWORD`:Salesforce password
- `SALESFORCE_TOKEN`: Salesforce security token
- `SALESFORCE_DOMAIN`: Optional: 'test' for a sandbox, or a custom domain.


### Disclaimer

This code works for me, but it’s offered “as is” without warranty. Use it at your own risk -- no liability is assumed by the authors for any issues in production.
