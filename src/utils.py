import os
from fyers_apiv3 import fyersModel

from dotenv import load_dotenv
import datetime as dt
import pandas as pd


def login(get_token=True, access_token=None):
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

    if get_token:
        generateTokenUrl = appSession.generate_authcode()
        print(generateTokenUrl, flush=True)

        auth_code = input("Enter Auth Code: ")
        appSession.set_token(auth_code)
    else:
        auth_code = os.getenv("AUTH_CODE")
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


def get_historical_data(
    fyers,
    ticker: str,
    resolution,
    start_date: dt.date,
    end_date: dt.date,
):
    days = (end_date - start_date).days
    prev = start_date
    final = -1

    def data_json(start, end):
        response = fyers.history(
            {
                "symbol": f"NSE:{ticker}-EQ",
                "resolution": resolution,
                "date_format": "1",
                "range_from": start,
                "range_to": end,
            }
        )
        df = pd.DataFrame(response["candles"])
        df.columns = ["ts", "Open", "High", "Low", "Close", "Volume"]
        df.index = pd.to_datetime(df.ts, unit="s")
        return df.drop(columns=["ts"])

    dfs = []
    for curr in range(min(100, days), days, 100):
        final = curr + 1

        data = data_json(prev, start_date + dt.timedelta(curr))
        dfs.append(data)
        prev = start_date + dt.timedelta(curr) + dt.timedelta(1)

    data = data_json(start_date + dt.timedelta(final), end_date)
    dfs.append(data)
    return pd.concat(dfs)
