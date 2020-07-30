from tests.credentials import creds
from readysignal import list_signals
from readysignal import connect_to_readysignal
from readysignal import fetch_signal_details
from readysignal import fetch_signal
from readysignal import fetch_signal_pandas
from readysignal.readysignal import ReadySignal
from pytest import fixture


@fixture
def list_signals_keys():
    """
    keys for dicts that the api returns
    :return: list of keys
    """
    return ['data', 'links', 'meta']


def list_signals_keys():
    """
    keys for dicts that the api returns
    :return: list of keys
    """
    return ['data', 'links', 'meta']


def test_connect_to_readysignal():
    """
    tests the API connection to Ready Signal

    :return: API connection or error
    """
    access_token = creds['access_token']
    rs = connect_to_readysignal(access_token)

    assert rs.ok


def test_list_signals():
    """
    tests an API call to get list of all signals a user owns

    :return: list of signal ids, or error
    """
    rs_instance = ReadySignal(creds['signal_id'])
    access_token = creds['access_token']
    signals = list_signals(access_token)

    assert isinstance(signals, dict)
    assert 'data' in signals.keys()


def test_fetch_signal_details():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal_details = fetch_signal_details(access_token, signal_id)
    print(fetch_signal_details(access_token, signal_id).keys())
    assert isinstance(signal_details, dict)
    assert 'data' in signal_details.keys()


def test_fetch_signal():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal = fetch_signal(access_token, signal_id)

    assert isinstance(signal, dict)
    assert 'data' in signal.keys()

def test_fetch_signal_pandas():
    access_token = creds['access_token']
    signal_id = creds['signal_id']
    signal = fetch_signal_pandas(access_token, signal_id)

    assert isinstance(signal, dict)
    assert 'data' in signal.keys()


test_connect_to_readysignal()
test_list_signals()
test_fetch_signal_details()
test_fetch_signal()
test_fetch_signal()
