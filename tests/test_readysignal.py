from tests.credentials import creds
from readysignal import connect_to_readysignal, list_signals, get_signal_details, delete_signal, auto_discover
from readysignal import get_signal, get_signal_pandas, signal_to_csv
from readysignal import connect_to_readysignal_features, get_features_list, show_feature, show_feature_detailed, get_feature_data, get_feature_data_pandas
import pandas as pd
import time


def test_connect_to_readysignal():
    """
    tests the API connection to Ready Signal

    :return: API connection or error
    """
    access_token = creds['access_token']
    rs = connect_to_readysignal(access_token)

    assert isinstance(rs, dict)


def test_list_signals():
    """
    tests an API call to get list of all signals a user owns

    :return: list of signal ids, or error
    """
    access_token = creds['access_token']
    signals = list_signals(access_token)

    assert isinstance(signals, dict)
    assert 'data' in signals.keys()

    return signals


def test_get_signal_details():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal_details = get_signal_details(access_token, signal_id)

    assert isinstance(signal_details, dict)
    assert 'data' in signal_details.keys()

    return signal_details


def test_get_signal():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal = get_signal(access_token, signal_id)

    assert isinstance(signal, list)
    assert 'start' in signal[0].keys()

    return signal


def test_get_signal_pandas():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal = get_signal_pandas(access_token, signal_id)

    assert isinstance(signal, type(pd.DataFrame()))
    assert 'start' in signal.columns

    return signal


def test_signal_to_csv():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    file_name = 'test1.csv'
    signal_to_csv(access_token, signal_id, file_name)

    return file_name


def test_auto_discover():
    access_token = creds['access_token']
    # response = auto_discover(access_token, 'Country', filename='../tests/country.csv')

    # assert response.status_code == 200

    response = auto_discover(access_token, 'Country', df=pd.read_csv('../tests/country.csv'))

    assert response.status_code == 200
    return response


def test_delete_signal(signal_id):
    access_token = creds['access_token']
    response = delete_signal(access_token, signal_id)

    assert response.status_code == 200
    return response

# tests for feature specific

def test_connect_to_readysignal_features():
    """
    tests the API connection to Ready Signal

    :return: API connection or error
    """
    access_token = creds['access_token_staging']
    rs = connect_to_readysignal_features(access_token)

    assert isinstance(rs, dict)

def test_get_features_list():
    """
    tests an API call to get list of all Bank of Mexico features

    :return: list of signal ids, or error
    """
    access_token = creds['access_token_staging']
    list_features = get_features_list(access_token)

    assert isinstance(list_features, dict)
    assert 'data' in list_features.keys()

    return list_features

def test_show_feature():
    """
    tests an API call to get list of all Bank of Mexico features

    :return: list of signal ids, or error
    """
    access_token = creds['access_token_staging']
    feature = 317
    feat_show = show_feature(access_token, feature)
    feat_dict = list(feat_show.values())[0]
   
    assert isinstance(feat_show, dict)
    assert 'data' in feat_show.keys()
    assert feature[0] in feat_dict.values()
    
    return feat_show

def test_show_feature_detailed():
    """
    tests an API call to get list of all Bank of Mexico features

    :return: list of signal ids, or error
    """
    access_token = creds['access_token_staging']
    feature = 317
    feat_details = show_feature_detailed(access_token, feature)
    feat_dict = list(feat_details.values())[0]

    assert isinstance(feat_details, dict)
    assert 'data' in feat_details.keys()
    assert feature[0] in feat_dict.values()

    return feat_details

def test_features_data():
    """
    tests an API call to get list of all Bank of Mexico features

    :return: list of signal ids, or error
    """
    access_token = creds['access_token_staging']
    feat_data = get_feature_data(access_token)

    assert isinstance(feat_data, dict)
    assert 'data' in feat_data.keys()

    return feat_data

def test_feature_data_pandas():
    """
    tests an API call to get list of all Bank of Mexico features

    :return: list of signal ids, or error
    """
    access_token = creds['access_token_staging']
    features = 317
    start_date = '2021-01-01'
    end_date = '2021-12-31'
    df = get_feature_data_pandas(access_token, features, start_date, end_date)

    assert isinstance(df, pd.DataFrame)

    return df

test_connect_to_readysignal()
test_list_signals()
test_get_signal_details()
test_get_signal()
print(test_get_signal_pandas())
test_signal_to_csv()
auto_disc = test_auto_discover().json()
test_delete_signal(auto_disc['signal_id'])
test_connect_to_readysignal_features()
test_get_features_list()
test_show_feature()
test_show_feature_detailed()
test_features_data()
test_feature_data_pandas()



