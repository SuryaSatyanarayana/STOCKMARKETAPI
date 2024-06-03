from kiteconnect import KiteConnect
import logging
from datetime import datetime, timedelta
import os
import json


def get_api_key():
    # Enable logging
    logging.basicConfig(level=logging.DEBUG)

    # Your API credentials
    api_key = "sfig85e573q89ytj"
    api_secret = "tms7bsqqtupluc08itmg97wpn8uevo5b"
    kite = KiteConnect(api_key=api_key)

    def save_access_token(token, file_path="access_token.json"):
        with open(file_path, "w") as f:
            json.dump({"access_token": token}, f)

    def load_access_token(file_path="access_token.json"):
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
                return data.get("access_token")
        return None

    # Load existing access token
    access_token = load_access_token()

    print(access_token)

    if access_token:
        kite.set_access_token(access_token)
        return kite
    else:
        # Step 1: Generate login URL and authenticate manually to get request token
        login_url = kite.login_url()
        print(f"Login URL: {login_url}")

        # Step 2: Manually open the login URL and authenticate to get request token
        request_token = input("Enter the request token: ")

        try:
            # Step 3: Generate session to get access token
            data = kite.generate_session(request_token, api_secret)
            access_token = data["access_token"]
            kite.set_access_token(access_token)

            # Save the access token for future use
            save_access_token(access_token)
        except Exception as e:
            logging.error(f"An error occurred during token generation: {e}")
    return kite
