import os
from simple_salesforce import Salesforce


def initialize_salesforce_api_client(username: str = None, password: str = None, security_token: str = None,
                                     domain: str = None) -> Salesforce:
    """
    Initialize the Salesforce API client using provided credentials or environment variables.
    """
    username = username or os.environ.get('SALESFORCE_EMAIL')
    password = password or os.environ.get('SALESFORCE_PASSWORD')
    security_token = security_token or os.environ.get('SALESFORCE_TOKEN')
    domain = domain or os.environ.get('SALESFORCE_DOMAIN') or 'login'

    return Salesforce(username=username, password=password, security_token=security_token, domain=domain)
