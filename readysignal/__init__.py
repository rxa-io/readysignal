import requests
import pandas as pd
import time


def connect_to_readysignal(access_token, signal_id=None, output=False, proxy_dict=None):
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
            url = f"http://app.readysignal.com/api/signals/{str(signal_id)}/output"
            headers = {
                "Authorization": "Bearer " + str(access_token),
                "Accept": "application/json",
            }

            req = requests.get(url, headers=headers, proxies=proxy_dict)

            if req.status_code != 200:
                print(
                    "Connection to Ready Signal failed. Check that your access token is up-to-date and signal ID is valid."
                )
                return

            resp = req.json()
            num_pages = resp["last_page"]

            for page in range(2, num_pages + 1):
                next_page = requests.get(
                    f"http://app.readysignal.com/api/signals/{str(signal_id)}/output",
                    headers=headers,
                    params={"page": page},
                    proxies=proxy_dict,
                ).json()
                resp["data"] += next_page["data"]
                time.sleep(1)

            return resp["data"]

        # list signals
        elif not signal_id:
            url = "http://app.readysignal.com/api/signals"

        # show signal details
        else:
            url = f"http://app.readysignal.com/api/signals/{str(signal_id)}"

        headers = {
            "Authorization": "Bearer " + str(access_token),
            "Accept": "application/json",
        }
        req = requests.get(url, headers=headers, proxies=proxy_dict)

        return req.json()
    except Exception as e:
        print("Connection to Ready Signal failed. Error:", e)
        return


def list_signals(access_token, proxy_dict=None):
    """
    lists all the signals associated with the user's access token
    :param access_token: user's unique access token
    :param proxy_dict: dictionary of the protocol to the proxy url
    :return: json of signals
    """
    conn = connect_to_readysignal(access_token, proxy_dict=proxy_dict)
    return conn


def get_signal_details(access_token, signal_id, proxy_dict=None):
    """
    shows the details for a specific signal
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :param proxy_dict: dictionary of the protocol to the proxy url
    :return: json of signal details
    """
    conn = connect_to_readysignal(access_token, signal_id, proxy_dict=proxy_dict)
    return conn


def get_signal(access_token, signal_id, proxy_dict=None):
    """
    returns a signal's data in json format
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :param proxy_dict: dictionary of the protocol to the proxy url
    :return: json of signal
    """
    conn = connect_to_readysignal(
        access_token, signal_id, proxy_dict=proxy_dict, output=True
    )
    return conn


def get_signal_pandas(access_token, signal_id, proxy_dict=None):
    """
    returns a signal's data as a Pandas DataFrame
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :param proxy_dict: dictionary of the protocol to the proxy url
    :return: Pandas DataFrame of signal
    """
    conn = connect_to_readysignal(
        access_token, signal_id, proxy_dict=proxy_dict, output=True
    )
    return pd.DataFrame.from_dict(conn)


def signal_to_csv(access_token, signal_id, file_name, proxy_dict=None):
    """
    returns a signal's data as a Pandas DataFrame
    :param file_name: name of file to write signal output to
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :param proxy_dict: dictionary of the protocol to the proxy url
    :return: Pandas DataFrame of signal
    """
    if "." in file_name and ".csv" not in file_name:
        exit('Please enter a file name in the format: "signal" or "signal.csv"')
    elif "." not in file_name:
        file_name += ".csv"

    output = get_signal_pandas(access_token, signal_id, proxy_dict=proxy_dict)
    output.to_csv(file_name, index=False)


def delete_signal(access_token, signal_id, proxy_dict=None):
    """
    USE WITH CAUTION. deletes a signal from the Ready Signal platform
    :param access_token: user's unique access token
    :param signal_id: signal's unique ID number
    :param proxy_dict: dictionary of the protocol to the proxy url
    :return: requests response object
    """
    url = f"http://app.readysignal.com/api/signals/{str(signal_id)}"

    headers = {
        "Authorization": "Bearer " + str(access_token),
        "Accept": "application/json",
    }
    req = requests.delete(url, proxies=proxy_dict, headers=headers)
    print(req.json())
    return req


def auto_discover(
    access_token,
    geo_grain,
    date_grain,
    proxy_dict=None,
    filename=None,
    df=None,
    create_custom_features=1,
):
    """
    Creates a signal using your own data and the Auto Discover feature. Please check Ready Signal site for tips on
    how to format your data. Currently only available at the "State" or "Country" geo grain.
    :param access_token: user's unique access token
    :param geo_grain: geographic grain of data upload: "State" or "Country"
    :param date_grain: date grain of data upload: "Day" or "Month"
    :param proxy_dict: dictionary of the protocol to the proxy url
    :param filename: if using file upload, filename. Accepted file formats: .CSV or .XLSX. Column naming schema should
    be "Date" (YYYY-MM-DD), "State" (MI) if geo_grain="State", "Value" (int or float, no strings).
    Not to be used with 'df'
    :param df: if using Pandas DataFrame upload, DataFrame object. Column naming schema should
    be "Date" (YYYY-MM-DD), "State" (MI) if geo_grain="State", "Value" (int or float, no strings).
    Not to be used with 'filename'
    :param create_custom_features: a flag to denote whether or not the target feature will be saved to the
    ready signal platform for reporting reference.
    :return: requests response object
    """
    base_url = "https://app.readysignal.com/api/auto-discovery"

    if geo_grain not in ["State", "Country"]:
        exit('Geographic grain for data must be "State" or "Country"')
    elif date_grain not in ["Day", "Month"]:
        exit('Date grain for data must be "Day" or "Month"')
    elif filename and df is not None:
        exit('Please use only one of "filename" or "df" for Auto Discover feature')
    elif create_custom_features not in [0, 1]:
        exit("Create Custom Features flag must be a 0 or a 1")

    elif filename:
        url = base_url + "/file"
        req = requests.post(
            url,
            data={
                "geo_grain": geo_grain,
                "date_grain": date_grain,
                "create_custom_features": create_custom_features,
            },
            files={"file": open(filename, "rb")},
            headers={"Authorization": "Bearer " + str(access_token)},
            proxies=proxy_dict,
        )
    elif df is not None:
        url = base_url + "/array"
        df["Date"] = df["Date"].astype(str)
        body = {
            "geo_grain": geo_grain,
            "date_grain": date_grain,
            "create_custom_features": create_custom_features,
            "data": df.to_dict(orient="records"),
        }

        req = requests.post(
            url,
            json=body,
            headers={"Authorization": "Bearer " + str(access_token)},
            proxies=proxy_dict,
        )

    else:
        exit(
            'Missing data source, please provide "filename" as filepath or "df" as Pandas dataframe'
        )

    return req


# functions for feature specific


def connect_to_readysignal_features(
    access_token,
    bank_name,
    features=None,
    start_date=None,
    end_date=None,
    details=False,
):
    """
    Pull data from specified bank datasets based on feature_id

    :param access_token: individual identification for readysignal
    :param type: string
    :param bank_name: country name of bank
    :param type: string
    :param features: list of feature_id(s)
    :param type: list of integer(s)
    :param start_date: start date for features
    :param type: string in Y-m-d format
    :param end_date: end_date for features
    :param type: string in Y-m-d format
    :param details: show feature details
    :param type: boolean
    :return: request response as json
    """
    lower_bank_name = bank_name.lower()
    try:
        # get feature(s) data
        if features and start_date and end_date:
            url = "https://app.readysignal.com/api/bank-of-" + lower_bank_name + "/data"
            headers = {
                "Authorization": "Bearer " + str(access_token),
                "Accept": "application/json",
            }
            body = {
                "start_date": str(start_date),
                "end_date": str(end_date),
                "features_id": features,
            }

            req = requests.post(url, headers=headers, json=body)

            return req.json()

        # show feature's details
        elif features and details:
            feat_details = {}
            for i in range(len(features)):
                url = (
                    "https://app.readysignal.com/api/bank-of-"
                    + lower_bank_name
                    + "/feature/"
                    + str(features[i])
                    + "/details"
                )
                headers = {
                    "Authorization": "Bearer " + str(access_token),
                    "Accept": "application/json",
                }
                req = requests.get(url, headers=headers)
                feat_details[features[i]] = list(req.json().values())[0]
            return feat_details

        # show feature's information
        elif features:
            feat_info = {}
            for i in range(len(features)):
                url = (
                    "https://app.readysignal.com/api/bank-of-"
                    + lower_bank_name
                    + "/feature/"
                    + str(features[i])
                )
                headers = {
                    "Authorization": "Bearer " + str(access_token),
                    "Accept": "application/json",
                }
                req = requests.get(url, headers=headers)
                feat_info[features[i]] = list(req.json().values())[0]
            return feat_info

        # list all bank features
        else:
            url = "https://app.readysignal.com/api/bank-of-" + lower_bank_name

        headers = {
            "Authorization": "Bearer " + str(access_token),
            "Accept": "application/json",
        }
        req = requests.get(url, headers=headers)

        return req.json()

    except Exception as e:
        print("Connection to Ready Signal failed. Error:", e)
        return


def get_features_list(access_token, bank_name):
    """
    List bank features available in the system for specified bank

    :param access_token: individual identification for readysignal
    :param type: string
    :param bank_name: country name of bank
    :param type: string
    :return: json of bank features
    """
    conn_features = connect_to_readysignal_features(access_token, bank_name)
    return conn_features


def show_feature(access_token, bank_name, features):
    """
    Show information on one feature

    :param access_token: individual identification for readysignal
    :param type: string
    :param bank_name: country name of bank
    :param type: string
    :param features: list of feature_id(s)
    :param type: list of integer(s)
    :return: json of bank of feature
    """
    conn_features = connect_to_readysignal_features(access_token, bank_name, features)
    return conn_features


def show_feature_detailed(access_token, bank_name, features):
    """
    Show detailed information about a specific feature

    :param access_token: individual identification for readysignal
    :param type: string
    :param bank_name: country name of bank
    :param type: string
    :param features: list of feature_id(s)
    :param type: list of integer(s)
    :return: json of a feature's details
    """
    conn_features = connect_to_readysignal_features(
        access_token, bank_name, features, details=True
    )
    return conn_features


def get_feature_data(access_token, bank_name, features, start_date, end_date):
    """
    Filter specified bank data by certain dates and feature_ids.

    :param access_token: individual identification for readysignal
    :param type: string
    :param bank_name: country name of bank
    :param type: string
    :param features: list of feature_id(s)
    :param type: list of integer(s)
    :param start_date: start date for features
    :param type: string in Y-m-d format
    :param end_date: end_date for features
    :param type: string in Y-m-d format
    :return: json of bank features data
    """
    conn_features = connect_to_readysignal_features(
        access_token, bank_name, features, start_date, end_date
    )
    return conn_features


def get_feature_data_pandas(access_token, bank_name, features, start_date, end_date):
    """
    returns a feature(s)'s data as a Pandas DataFrame

    :param access_token: individual identification for readysignal
    :param type: string
    :param bank_name: country name of bank
    :param type: string
    :param features: list of feature_id(s)
    :param type: list of integer(s)
    :param start_date: start date for features
    :param type: string in Y-m-d format
    :param end_date: end_date for features
    :return: Pandas DataFrame of signal
    """

    conn_features = connect_to_readysignal_features(
        access_token, bank_name, features, start_date, end_date
    )
    data = list(conn_features.values())
    df = pd.DataFrame(columns=list(data[0][0].keys()))
    for i in range(len(data[0])):
        df.loc[len(df.index)] = list(data[0][i].values())
    return df
