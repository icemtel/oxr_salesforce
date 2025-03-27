def test_oxr_connection():
    from oxr_salesforce.oxr import get_exchange_rate_latest

    # Test that we can fetch exchange rates from the API
    rate = get_exchange_rate_latest('USD', 'EUR')
    assert rate > 0


def test_salesforce_connection():
    import os
    from simple_salesforce import Salesforce
    # Test that we can connect to Salesforce
    username = os.environ.get('SALESFORCE_EMAIL')
    security_token = os.environ.get('SALESFORCE_TOKEN')
    password = os.environ.get('SALESFORCE_PASSWORD')
    domain = os.environ.get('SALESFORCE_DOMAIN')
    sf = Salesforce(username=username, password=password, security_token=security_token, domain=domain)


    # Simple query to verify connection
    query = """
    SELECT Id, IsoCode, ConversionRate, IsCorporate
    FROM CurrencyType
    LIMIT 1
    """
    result = sf.query(query)
    assert result['done']