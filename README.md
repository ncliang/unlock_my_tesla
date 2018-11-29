# unlock_my_tesla
Small script to loop and unlock my Tesla when the car is at home.

Makes use of myTesla.py from https://github.com/zmsp/python-my-tesla.

```
usage: unlock_my_tesla.py [-h] --username USERNAME [--interval INTERVAL]

Unlock my tesla.

optional arguments:
  -h, --help           show this help message and exit
  --username USERNAME  Tesla username
  --interval INTERVAL  Polling interval in seconds
```
The script will prompt for your Tesla password each time it is launched but will not save it anywhere.
