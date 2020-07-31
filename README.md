# ReadySignal API

## Installation

```shell script
python -m pip install {path to directory}/dist/readysignal-0.2-py3-none-any.whl
```

```shell script
pip install readysignal
```

###Command



## Usage

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