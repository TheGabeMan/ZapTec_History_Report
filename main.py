# Main Script for ZapTec API
import os
import requests
from datetime import datetime, timedelta


def main():
    """ The Main Script """
    username = os.getenv('username')
    password = os.getenv('password')
    apiurl = 'https://api.zaptec.com'

    access_token = authenticate(username, password, apiurl)
    print(access_token)

    charge_history = get_charge_history(access_token=access_token, apiurl=apiurl)
    print(charge_history)


def get_charge_history(access_token, apiurl, start_date=None, end_date=None, max_entries=100):
    """
    Retrieve charge history from Zaptec ZapCloud
    :param start_date: Start date for charge history (default: 30 days ago)
    :param end_date: End date for charge history (default: today)
    :param max_entries: Maximum number of entries to retrieve
    :return: List of charge history entries
    """

    # Default to last 30 days if no dates specified
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()

    history_url = f"{apiurl}/api/chargehistory"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "StartDate": start_date.isoformat(),
        "EndDate": end_date.isoformat(),
        "MaxEntires": max_entries
    }

    try:
        response = requests.get(history_url, headers=headers, params=params)
        response.raise_for_status()
        charge_history = response.json()
        return charge_history
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve charge history: {e}")
        return []


def authenticate(username, password, apiurl):
    """
    Authenticate and obtain access token
    """

    auth_url = f"{apiurl}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password
        # "client_id": "ZaptecPortal"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(auth_url, data=payload, headers=headers)
        response.raise_for_status()

        auth_data = response.json()
        access_token = auth_data.get('access_token')
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"Authentication failed: {e}")
        return False

if __name__ == "__main__":
    main()
