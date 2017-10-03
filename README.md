# coin-counter
A Flask app for viewing account info from the Coinbase API.

## Running the App
First, you have to generate your own API key and secret through [Coinbase](https://coinbase.com/settings/api) with the appropriate permissions (at least `wallet:accounts:read` and `wallet:transactions:read`. Copy and paste these keys into the appropriate lines in `api_keys.py`. 

**Note: Do NOT share these keys with anyone; they are for your own personal     use.** 

Then, run the following commands from the repository directory to start the app, which runs on localhost by default.

```
$ pip install coinbase
$ python app.py
```
