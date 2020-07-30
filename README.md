# ReadySignal API

## Installation

```shell script
python -m pip install {path to directory}/dist/readysignal-0.1-py3-none-any.whl
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

signal = rs.get_signal(access_token, signal_id)

print(signal)
```