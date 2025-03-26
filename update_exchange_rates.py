"""
Update the latest currency exchange rate in a Salesforce org.
"""
from datetime import date
from sf import initialize_salesforce_api_client, Salesforce
from oxr import get_exchange_rate_latest
from log import setup_logging

# Setup logger
logger = setup_logging()


def _validate_currencies(base_currency: str, target_currency: str, sf: Salesforce) -> dict:
    """
    Validate that both currencies exist in the organization and that the base currency is the corporate currency.
        
    Returns:
        dict: Dictionary containing currency data for both currencies
        
    Raises:
        ValueError: If any validation check fails
    """
    # Fetch all relevant currencies in one query
    query = f"""
    SELECT Id, IsoCode, ConversionRate, IsCorporate
    FROM CurrencyType
    WHERE IsoCode IN ('{base_currency}', '{target_currency}')
    """
    currency_result = sf.query(query)
    
    # Create a dictionary to easily access currency data by ISO code
    currencies = {record['IsoCode']: record for record in currency_result['records']}
    
    # Check if both currencies exist in the organization
    if base_currency not in currencies:
        raise ValueError(f"Base currency {base_currency} was not found in Salesforce.")
    
    if target_currency not in currencies:
        raise ValueError(f"Target currency {target_currency} was not found in Salesforce.")
    
    # Check if base currency is the corporate currency
    if not currencies[base_currency].get('IsCorporate'):
        raise ValueError(f"Base currency {base_currency} is not the corporate currency in Salesforce.")
    
    return currencies


def update_current_rate(base_currency: str, target_currency: str, sf: Salesforce):
    """
    Update current exchange rates for a single currency.

    Args:
        base_currency: ISO code of the base currency
        target_currency: ISO code of the target currency
        sf: Salesforce client from the `simple_salesforce` package
    """
    # Validate currencies in Salesforce and get currency data
    currencies = _validate_currencies(base_currency, target_currency, sf)
    target_currency_id = currencies[target_currency]['Id']

    # Get latest exchange rate
    try:
        rate = get_exchange_rate_latest(base_currency, target_currency)
    except Exception as e:
        logger.error("Failed to fetch current exchange rate")
        raise e

    # Update the target currency with the new rate
    try:
        sf.CurrencyType.update(target_currency_id, {'ConversionRate': str(rate)})
        logger.info(f"Updated CurrencyType")
    except Exception as e:
        logger.error(f"Failed to update CurrencyType record for currency {target_currency} in Salesforce.")
        raise e
    
    # Prepare data for dated conversion rate
    today = date.today()

    record = {
        'IsoCode': target_currency,
        'ConversionRate': str(rate),
        'StartDate': str(today)
    }

    # Create the dated conversion rate, or update it if already exists
    try:
        query_results = sf.query(
        f"SELECT Id FROM DatedConversionRate WHERE IsoCode = '{target_currency}' AND StartDate = {today}"
        )
        if query_results['totalSize'] == 0:   # Create new record
            sf.DatedConversionRate.create(record)
            logger.info(f"Created new DatedConversionRate")
        else: # Update existing record
            record_id = query_results['records'][0]['Id']
            sf.DatedConversionRate.update(record_id, {'ConversionRate': str(rate)})
            logger.info(f"Updated existing DatedConversionRate")

    except Exception as e:
        logger.error(f"Failed to update dated currency rate.")
        raise e


if __name__ == '__main__':
    base_currency = 'USD'
    target_currency = 'EUR'

    sf = initialize_salesforce_api_client()
    update_current_rate(base_currency, target_currency, sf)
