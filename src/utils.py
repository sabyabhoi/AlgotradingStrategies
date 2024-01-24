import os
from fyers_apiv3 import fyersModel

from dotenv import load_dotenv


def login():
    load_dotenv()
    redirect_url = os.getenv("REDIRECT_URL")
    client_id = os.getenv("CLIENT_ID")
    secret_key = os.getenv("SECRET_KEY")
    grant_type = "authorization_code"
    response_type = "code"
    state = "sample"

    appSession = fyersModel.SessionModel(
        client_id=client_id,
        redirect_uri=redirect_url,
        response_type=response_type,
        secret_key=secret_key,
        grant_type=grant_type,
        state=state,
    )

    generateTokenUrl = appSession.generate_authcode()
    print(generateTokenUrl, flush=True)

    auth_code = input("Enter Auth Code: ")
    appSession.set_token(auth_code)

    response = appSession.generate_token()

    try:
        access_token = response["access_token"]
    except Exception as e:
        print(e, response)

    fyers = fyersModel.FyersModel(
        token=access_token, is_async=False, client_id=client_id
    )
    return (access_token, fyers)
