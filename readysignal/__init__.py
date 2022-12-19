import requests
import pandas as pd
import time
import json


def connect_to_readysignal(access_token, signal_id=None, output=False):
    """
    creates connection to correct API URL to list signals, show signal
    details, and return complete signal data
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number, to show signal details
    or output full signal
    :param output: show signal data or not
    :return: request response as json
    """
    try:
        # show signal
        if signal_id and output:
            url = f'http://app.readysignal.com/api/signals/{str(signal_id)}/output'
            headers = {'Authorization': 'Bearer ' + str(access_token),
                       'Accept': 'application/json'}

            req = requests.get(url, headers=headers)

            if req.status_code != 200:
                print(
                    'Connection to Ready Signal failed. Check that your access token is up-to-date and signal ID is valid.')
                return

            resp = req.json()
            num_pages = resp['last_page']

            for page in range(2, num_pages + 1):
                next_page = requests.get(f'http://app.readysignal.com/api/signals/{str(signal_id)}/output',
                                         headers=headers,
                                         params={'page': page}).json()
                resp['data'] += next_page['data']
                time.sleep(1)

            return resp['data']

        # list signals
        elif not signal_id:
            url = 'http://app.readysignal.com/api/signals'

        # show signal details
        else:
            url = f'http://app.readysignal.com/api/signals/{str(signal_id)}'

        headers = {'Authorization': 'Bearer ' + str(access_token),
                   'Accept': 'application/json'}
        req = requests.get(url, headers=headers)

        return req.json()
    except Exception as e:
        print('Connection to Ready Signal failed. Error:', e)
        return


def list_signals(access_token):
    """
    lists all the signals associated with the user's access token
    :param access_token: user's unique access token
    :return: json of signals
    """
    conn = connect_to_readysignal(access_token)
    return conn


def get_signal_details(access_token, signal_id):
    """
    shows the details for a specific signal
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: json of signal details
    """
    conn = connect_to_readysignal(access_token, signal_id)
    return conn


def get_signal(access_token, signal_id):
    """
    returns a signal's data in json format
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: json of signal
    """
    conn = connect_to_readysignal(access_token, signal_id, output=True)
    return conn


def get_signal_pandas(access_token, signal_id):
    """
    returns a signal's data as a Pandas DataFrame
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: Pandas DataFrame of signal
    """
    conn = connect_to_readysignal(access_token, signal_id, output=True)
    return pd.DataFrame.from_dict(conn)


def signal_to_csv(access_token, signal_id, file_name):
    """
    returns a signal's data as a Pandas DataFrame
    :param file_name: name of file to write signal output to
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: Pandas DataFrame of signal
    """
    if '.' in file_name and '.csv' not in file_name:
        exit('Please enter a file name in the format: "signal" or "signal.csv"')
    elif '.' not in file_name:
        file_name += '.csv'

    output = get_signal_pandas(access_token, signal_id)
    output.to_csv(file_name, index=False)


def delete_signal(access_token, signal_id):
    """
    USE WITH CAUTION. deletes a signal from the Ready Signal platform
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :return: requests response object
    """
    url = f'http://app.readysignal.com/api/signals/{str(signal_id)}'

    headers = {'Authorization': 'Bearer ' + str(access_token),
               'Accept': 'application/json'}
    req = requests.delete(url, headers=headers)
    print(req.json())
    return req


def auto_discover(access_token, geo_grain, filename=None, df=None):
    """
    Creates a signal using your own data and the Auto Discover feature. Please check Ready Signal site for tips on
    how to format your data. Currently only available at the "State" or "Country" geo grain.
    :param access_token: user's unique access token
    :param geo_grain: geographic grain of data upload: "State" or "Country"
    :param filename: if using file upload, filename. Accepted file formats: .CSV or .XLSX. Column naming schema should
    be "Date" (YYYY-MM-DD), "State" (MI) if geo_grain="State", "Value" (int or float, no strings).
    Not to be used with 'df'
    :param df: if using Pandas DataFrame upload, DataFrame object. Column naming schema should
    be "Date" (YYYY-MM-DD), "State" (MI) if geo_grain="State", "Value" (int or float, no strings).
    Not to be used with 'filename'
    :return: requests response object
    """
    base_url = 'https://app.readysignal.com/api/auto-discovery'

    if geo_grain not in ['State', 'Country']:
        exit('Geographic grain for data must be "State" or "Country"')
    elif filename and df is not None:
        exit('Please use only one of "filename" or "df" for Auto Discover feature')

    elif filename:
        url = base_url + '/file'
        req = requests.post(url, data={'geo_grain': geo_grain}, files={'file': open(filename, 'rb')},
                            headers={'Authorization': 'Bearer ' + str(access_token)})
    elif df is not None:
        url = base_url + '/array'
        body = {"geo_grain": geo_grain, "data": df.to_dict(orient='records')}

        req = requests.post(url, json=body, headers={'Authorization': 'Bearer ' + str(access_token)})

    else:
        exit('Missing data source, please provide "filename" as filepath or "df" as Pandas dataframe')
    print(req.json())
    return req
