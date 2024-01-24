from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws

from dotenv import load_dotenv

from utils import login


class TickHandler:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def onmessage(self, message: dict):
        """
        Callback function to handle incoming messages from the FyersDataSocket WebSocket.

        Parameters:
            message (dict): The received message from the WebSocket.

        """
        print("Response:", message)

    def onerror(self, message: dict):
        """
        Callback function to handle WebSocket errors.

        Parameters:
            message (dict): The error message received from the WebSocket.


        """
        print("Error:", message)

    def onclose(self, message):
        """
        Callback function to handle WebSocket connection close events.
        """
        print("Connection closed:", message)

    def onopen(self):
        """
        Callback function to subscribe to data type and symbols upon WebSocket connection.

        """
        data_type = "SymbolUpdate"

        # Subscribe to the specified symbols and data type
        symbols = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
        self.fyers.subscribe(symbols=symbols, data_type=data_type)

        # Keep the socket running to receive real-time data
        self.fyers.keep_running()

    def connect(self):
        self.fyers = data_ws.FyersDataSocket(
            access_token=self.access_token,  # Access token in the format "appid:accesstoken"
            log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
            litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
            write_to_file=False,  # Save response in a log file instead of printing it.
            reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
            on_connect=self.onopen,  # Callback function to subscribe to data upon connection.
            on_close=self.onclose,  # Callback function to handle WebSocket connection close events.
            on_error=self.onerror,  # Callback function to handle WebSocket errors.
            on_message=self.onmessage,  # Callback function to handle incoming messages from the WebSocket.
        )
        fyers.connect()


if __name__ == "__main__":
    load_dotenv()

    access_token, fyers = login()

    handler = TickHandler(access_token=access_token)
    handler.connect()
