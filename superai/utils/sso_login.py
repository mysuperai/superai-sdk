import configparser
import time
import webbrowser
from pathlib import Path

from boto3.session import Session


def sso_login(account_name: str, role_name: str, start_url: str, region: str):
    """Login to AWS SSO and save temporary credentials to ~/.aws/credentials file."""
    session = Session()
    sso_oidc = session.client("sso-oidc")

    client_creds = sso_oidc.register_client(clientName="superai", clientType="public")
    device_authorization = sso_oidc.start_device_authorization(
        clientId=client_creds["clientId"],
        clientSecret=client_creds["clientSecret"],
        startUrl=start_url,
    )
    url = device_authorization["verificationUriComplete"]
    device_code = device_authorization["deviceCode"]
    expires_in = device_authorization["expiresIn"]
    interval = device_authorization["interval"]
    webbrowser.open(url, autoraise=True)
    # Wait for the user to confirm SSO access in the web browser
    for _ in range(1, expires_in // interval + 1):
        time.sleep(interval)
        try:
            token = sso_oidc.create_token(
                grantType="urn:ietf:params:oauth:grant-type:device_code",
                deviceCode=device_code,
                clientId=client_creds["clientId"],
                clientSecret=client_creds["clientSecret"],
            )
            break
        except sso_oidc.exceptions.AuthorizationPendingException:
            pass

    access_token = token["accessToken"]
    sso = session.client("sso")
    account_list = sso.list_accounts(accessToken=access_token)

    accounts = {account["accountName"]: account["accountId"] for account in account_list["accountList"]}
    account_id = accounts.get(account_name)
    if account_id is None:
        print(f"Account name {account_name} is not a valid account. Possible accounts {list(accounts)}")

    account_roles = sso.list_account_roles(accessToken=access_token, accountId=account_id)
    role_names = [role["roleName"] for role in account_roles["roleList"]]
    if role_name not in role_names:
        print(f"Role {role_name} is not a valid role. Possible roles {role_names}")
        return

    role_credentials = sso.get_role_credentials(
        roleName=role_name,
        accountId=account_id,
        accessToken=access_token,
    )
    credentials = role_credentials["roleCredentials"]

    # Write temporary credentials to ~/.aws/credentials file
    config = configparser.ConfigParser()

    credentials_file = Path.home() / ".aws/credentials"
    config.read(credentials_file)

    config[account_name.lower()] = {
        "region": region,
        "aws_access_key_id": credentials["accessKeyId"],
        "aws_secret_access_key": credentials["secretAccessKey"],
        "aws_session_token": credentials["sessionToken"],
    }

    with open(credentials_file, "w") as config_file:
        config.write(config_file)

    print(f"Temporary AWS credentials saved to {credentials_file}")
