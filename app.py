from coinbase.wallet.client import Client
from flask import Flask, render_template
from api_keys import *
import json

app = Flask(__name__)
client = Client(API_KEY, API_SECRET)

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

@app.route("/")
def index():
    accountDict = {}
    accounts = client.get_accounts()

    for account in accounts.data:

        # Get total, profit, and rates
        transactionSum = sumTransactions(account)
        profit = float(account.native_balance.amount) - transactionSum
        transactions = account.get_transactions().data
        for trans in transactions:
            trans["rate"] = getTransactionRate(trans)
            trans["amount"]["amount"] = float(trans["amount"]["amount"])
            if "Sold" in trans["details"]["title"]:
                trans["profit"] = "-"
            else:
                trans["profit"] = "%.2f" % getTransactionProfit(trans)

        # Format the data for the front end
        accountDict[str(account.balance.currency)] = {
            "nativeSpent": transactionSum,
            "nativeWorth": account.native_balance.amount,
            "nativeCurrency": account.native_balance.currency,
            "profit": float(account.native_balance.amount) - transactionSum,
            "transactions": transactions
        }
        rates = client.get_exchange_rates()
        for crypto in accountDict.keys():
            rates["rates"][crypto] = float(rates["rates"][crypto])

    return render_template("index.html", accountDict=accountDict, rates=rates)

if __name__ == "__main__":
    app.run(debug=True)