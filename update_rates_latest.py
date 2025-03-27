"""
Update the latest currency exchange rate in a Salesforce org.
"""
from datetime import date
from sf import initialize_salesforce_api_client, Salesforce
from oxr import get_exchange_rate_latest
from log import setup_logging

# Setup logger
logger = setup_logging()


def _find_dict(list_of_dicts, key, value):
    """
    In a list of dictionaries, finds the first dictionary that satisfies the key-value pair match.
    Returns None if nothing found.
    """
    return next((d for d in list_of_dicts if d.get(key) == value), None)


def get_salesforce_currencies(sf: Salesforce):
    """
    Returns:
        str: ISO code of the corporate currency
        list: list of dicts (keys: Salesforce field names, values - field values from Salesforce)
    """
    # Fetch all relevant currencies
    query = f"""
    SELECT Id, IsoCode, ConversionRate, IsCorporate
    FROM CurrencyType
    """
    try:
        query_response = sf.query(query)
        records = query_response['records']
    except Exception as e:
        logger.error(f"Failed to fetch existing currencies from Salesforce.")
        raise e

    if query_response['totalSize'] <= 1:
        raise Exception(
            f"Missing target currencies: {query_response['totalSize']} CurrencyType record(s) found in Salesforce.")

    base_currency_record = _find_dict(records, 'IsCorporate', True)

    if base_currency_record is None:
        raise Exception(f"Failed to find corporate currency in Salesforce.")

    base_currency = base_currency_record.get('IsoCode')
    target_currencies_data = [rec for rec in records if rec.get('IsCorporate') is False]

    return base_currency, target_currencies_data


def get_salesforce_dated_conversion_rates(d: date, sf: Salesforce):
    query = f"SELECT Id, IsoCode FROM DatedConversionRate WHERE StartDate = {d}"

    try:
        query_response = sf.query(query)
        records = query_response['records']
    except Exception as e:
        logger.error(f"Failed to fetch dated conversion rates from Salesforce for date {d}.")
        raise e

    return records


def update_current_rates(sf: Salesforce):
    """
    Update current exchange rates for a single currency.

    Args:
        base_currency: ISO code of the base currency. Must be the corporate currency of the Salesforce org.
        target_currencies: list of ISO code of the target currency
        sf: Salesforce client from the `simple_salesforce` package
    """
    # Validate currencies in Salesforce and get currency data
    base_currency, target_currencies_existing_records = get_salesforce_currencies(sf)
    # Get latest exchange rate & prepare data to update CurrencyType records

    currency_types_to_update = []  # list of dicts
    rates = {}  # keys: currency iso codes; we'll need this dictionary later
    for rec in target_currencies_existing_records:
        try:
            target_currency = rec['IsoCode']
            rate = get_exchange_rate_latest(base_currency, target_currency)

            currency_types_to_update.append(
                {'Id': rec['Id'],
                 'ConversionRate': str(rate),
                 }
            )

            rates[target_currency] = str(rate)

        except Exception as e:
            logger.error(f"Failed to fetch current exchange rate for {target_currency}")
            raise e

    # Update CurrencyType records
    try:
        results = sf.bulk.CurrencyType.update(currency_types_to_update)
    except Exception as e:
        logger.error(f"Failed to update CurrencyType records in Salesforce.")
        raise e

    # Check for errors
    failed_records = [record for record in results if not record.get('success')]
    if failed_records:
        for rec in failed_records:
            rec_id = rec.get('id', 'Unknown ID')
            target_currency = _find_dict(target_currencies_existing_records, 'Id', rec_id).get('IsoCode', '<Unknown>')

            error_message = rec.get('errors', [{}])[0].get('message', '<Unknown>')
            logger.error(f"Failed to update CurrencyType for currency {target_currency}: '{error_message}'")

        raise Exception("Failed to update some CurrencyType records.")
    else:
        logger.info(f"Updated {len(currency_types_to_update)} CurrencyType records.")

    # Create the dated conversion rate, or update it if already exists
    today = date.today()
    existing_dated_conversion_rates = get_salesforce_dated_conversion_rates(today, sf)

    # Split records into those to update and those to create
    records_to_update = []
    records_to_create = []

    # Get the IsoCode for each record from the target_currencies_existing_records
    for target_currency, rate in rates.items():
        # Find if there's an existing dated conversion rate record with the same ISO code
        existing_record = _find_dict(existing_dated_conversion_rates, 'IsoCode', target_currency)

        if existing_record:
            # If exists, prepare for update with the existing ID
            update_record = {
                'Id': existing_record['Id'],
                'ConversionRate': rate
            }
            records_to_update.append(update_record)
        else:
            # If doesn't exist, prepare for creation
            create_record = {
                'IsoCode': target_currency,
                'ConversionRate': rate,
                'StartDate': str(today)
            }
            records_to_create.append(create_record)

    # Perform bulk update if there are records to update
    if records_to_update:
        try:
            update_results = sf.bulk.DatedConversionRate.update(records_to_update)
            # Check for failed updates
            failed_updates = [record for record in update_results if not record.get('success')]
            if failed_updates:
                for rec in failed_updates:
                    rec_id = rec.get('id', 'Unknown ID')
                    error_message = rec.get('errors', [{}])[0].get('message', '<Unknown>')
                    logger.error(f"Failed to update DatedConversionRate with ID {rec_id}: '{error_message}'")
                raise Exception("Failed to update some DatedConversionRate records.")
            else:
                logger.info(f"Updated {len(records_to_update)} DatedConversionRate records")
        except Exception as e:
            logger.error(f"Failed to perform bulk update of DatedConversionRate records: {str(e)}")
            raise e

    # Perform bulk insert if there are records to create
    if records_to_create:
        try:
            create_results = sf.bulk.DatedConversionRate.insert(records_to_create)

            # Check for failed inserts
            failed_inserts = [record for record in create_results if not record.get('success')]
            if failed_inserts:
                for rec in failed_inserts:
                    error_message = rec.get('errors', [{}])[0].get('message', '<Unknown>')
                    logger.error(f"Failed to create DatedConversionRate: '{error_message}'")
                raise Exception("Failed to create some DatedConversionRate records.")
            else:
                logger.info(f"Created {len(records_to_create)} DatedConversionRate records")
        except Exception as e:
            logger.error(f"Failed to perform bulk insert of DatedConversionRate records: {str(e)}")
            raise e


if __name__ == '__main__':
    sf = initialize_salesforce_api_client()
    update_current_rates(sf)
