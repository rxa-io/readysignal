# ReadySignal API - Python 3.6+
This library is designed to be a wrapper for the ReadySignal API: http://app.readysignal.com

Please direct all questions and/or recommendations to jess.brown@rxa.io.

## Installation

```shell script
pip install readysignal
```

## Usage
Your access token can be found on your "Manage Signal" page within the Output information.
The signal id can be found either within the Output information or in the URL of the 
"Manage Signal" page: https://staging.app.readysignal.com/signal/{signal_id}/manage.
```python
import readysignal as rs

access_token = "your access token"
signal_id = 0

# list signals
rs.list_signals(access_token)

# get signal details
rs.get_signal_details(access_token, signal_id)

# get signal data as json
rs.get_signal(access_token, signal_id)

# get signal data as Pandas DataFrame
rs.get_signal_pandas(access_token, signal_id)
```