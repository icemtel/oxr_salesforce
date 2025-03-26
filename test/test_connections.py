import pytest

def test_oxr_connection():
    from oxr import get_exchange_rate_latest

    # Test that we can fetch exchange rates from the API
    rate = get_exchange_rate_latest('USD', 'EUR')
    assert rate > 0


def test_salesforce_connection():
    from sf import initialize_salesforce_api_client

    # Test that we can connect to Salesforce
    sf = initialize_salesforce_api_client()

    # Simple query to verify connection
    query = """
    SELECT Id, IsoCode, ConversionRate, IsCorporate
    FROM CurrencyType
    LIMIT 1
    """
    result = sf.query(query)
    assert result['done']