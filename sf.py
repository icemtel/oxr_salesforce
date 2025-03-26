from simple_salesforce import Salesforce
import os


def initialize_salesforce_api_client(email: str = None, security_token: str = None, password: str = None, sandbox: str = None):
    """
    Initialize the Salesforce API client using provided credentials or environment variables.
    If a sandbox is specified, appends its name to the email and connects to the test domain.
    """
    email = email or os.environ.get('SALESFORCE_EMAIL')
    security_token = security_token or os.environ.get('SALESFORCE_TOKEN')
    password = password or os.environ.get('SALESFORCE_PASSWORD')
    sandbox = sandbox or os.environ.get('SALESFORCE_SANDBOX')

    if not all([email, security_token, password]):
        raise RuntimeError("Missing one or more required Salesforce credentials (email, security_token, or password).")

    if sandbox:
        email = f"{email}.{sandbox}"  # Format for sandbox login.
        domain = 'test'
    else:
        domain = None

    return Salesforce(username=email, password=password, security_token=security_token, domain=domain)