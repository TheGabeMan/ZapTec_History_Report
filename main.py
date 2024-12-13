# Main Script for ZapTec API
import os
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import storage


def main():
    """ The Main Script """
    username = os.getenv('username')
    password = os.getenv('password')
    chargerdid = os.getenv('chargerid')
    installationid = os.getenv('InstallationId')
    apiurl = 'https://api.zaptec.com'

    access_token = authenticate(username, password, apiurl)
    # print(access_token)

    charge_history = get_charge_history_installation(access_token=access_token, apiurl=apiurl, installationid=installationid, GroupBy=1)
    for key in charge_history['Data']:
        print(key)
        sql_error = storage.sql_insert(key=key)

        if sql_error:
            print('Error when storing data in database')
            exit

        ## Mail data

        # UserUserName
        # Id
        # DeviceID
        # StartDateTime
        # EndDateTime
        # Energy
        # UserFullName
        # ChargerId
        # DeviceName
        # UserEmail
        # UserId


def get_charge_history_installation(access_token, apiurl, installationid, GroupBy=0, DetailLevel=0, max_entries=200):
    """
    Retrieve charge history from Zaptec ZapCloud
    :param start_date: Start date for charge history (default: 30 days ago)
    :param end_date: End date for charge history (default: today)
    :param max_entries: Maximum number of entries to retrieve
    :param GroupBy 0 = 
    :return: List of charge history entries
    """

    # Default to last 30 days if no dates specified
    # start_date, end_date = get_previous_month_dates()
    start_date, end_date = get_current_month_dates()

    history_url = f"{apiurl}/api/chargehistory"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    params = {
        "StartDate": start_date.isoformat(),
        "EndDate": end_date.isoformat(),
        "MaxEntires": max_entries,
        "InstallationId": installationid,
        "GroupBy": GroupBy,
        "DetailLevel": DetailLevel
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


def get_previous_month_dates():
    # Get current date in UTC
    current_date = datetime.now(ZoneInfo("UTC"))
    first_day_current_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_previous_month = first_day_current_month - timedelta(days=1, hour=0, minute=0, second=0, microsecond=0)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    return first_day_previous_month, last_day_previous_month


def get_current_month_dates():
    # Get current date in UTC
    current_date = datetime.now(ZoneInfo("UTC"))
    first_day_current_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if current_date.month == 12:
        last_day_current_month = current_date.replace(year=current_date.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        last_day_current_month = current_date.replace(month=current_date.month + 1, day=1) - timedelta(days=1)
    last_day_current_month = last_day_current_month.replace(hour=0, minute=0, second=0, microsecond=0)
    return first_day_current_month, last_day_current_month


if __name__ == "__main__":
    main()
