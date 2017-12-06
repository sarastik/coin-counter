from coinbase.wallet.client import Client
from flask import Flask, render_template
from api_keys import *
import requests
import json
import csv

app = Flask(__name__)
client = Client(API_KEY, API_SECRET)

EXCHANGES_TO_DISPLAY = ["BTC", "ETH", "LTC", "VTC", "BCH", "XMR", "XRP"]
EXCHANGE_TO = "USD"
BITTREX_MARKETS_ENDPOINT = "https://bittrex.com/api/v1.1/public/getmarkets"
CSV_FILEPATH = "wallet.csv"

def sumTransactions(account):
    """
    Takes in account object and returns the total native currency spent on that wallet.
    This includes the total amount of native currency spent minus the amount received if any was sold.
    """
    transactions = account.get_transactions()
    transactionTotal = 0
    for trans in transactions.data:
        transactionTotal += float(trans.native_amount.amount)
    return transactionTotal

def getTransactionRate(trans):
    """
    Given a transaction object (from the "data" list returned by get_transactions API call), 
    returns the worth of the cryptocurrency in the native currency at the transaction time.
    """
    crypto = abs(float(trans.amount.amount))
    native = abs(float(trans.native_amount.amount))
    return native / crypto

def getTransactionProfit(trans, nativeSell=50, cryptoSell=None):
    """
    Given a transaction object (from the "data" list returned by get_transactions API call),
    returns the potential native profit received by selling the specified amount at the current time.
    """
    originalRate = getTransactionRate(trans)
    currentRate = 1 / float(client.get_exchange_rates()["rates"][trans.amount.currency])
    
    if cryptoSell:
        profit = (cryptoSell * currentRate) - (cryptoSell * originalRate)
    else:
        nativeAtOriginalRate = (nativeSell * (1 / currentRate)) * originalRate
        profit = nativeSell - nativeAtOriginalRate
    return profit

def getExchangeRatesToDisplay(exchangesToDisplay, exchangeTo):
    """
    Given a list of currencies to display and a currency to exchange to, 
    returns the API response containing current exchange rates for currencies specified. 
    """
    requestUrl = "https://min-api.cryptocompare.com/data/pricemulti?fsyms={}&tsyms={}".format(
        ",".join(exchangesToDisplay),
        exchangeTo
    )

    response = requests.get(requestUrl)
    responseDict = json.loads(response.text)
    return responseDict

def getProfitsFromCSV(filePath):
    coinsToDollarsOwned = {}
    with open(filePath, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        reader.next()
        for row in reader:
            coinsToDollarsOwned[row[0]] = {"dollarsSpent": row[1], "coinsOwned": row[2]}
    
    #TODO: get exchange rates * amount owned and compare to dollars spent

@app.route("/")
def index():
    accountDict = {}
    accounts = client.get_accounts()

    exchangeDict = getExchangeRatesToDisplay(EXCHANGES_TO_DISPLAY, EXCHANGE_TO)

    

    return render_template("index.html", exchangeDict=exchangeDict, 
                                         exchangeOrder=EXCHANGES_TO_DISPLAY,
                                         exchangeTo=EXCHANGE_TO)

if __name__ == "__main__":
    app.run(debug=True)