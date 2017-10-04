from coinbase.wallet.client import Client
from flask import Flask, render_template
from api_keys import *
import json

app = Flask(__name__)
client = Client(API_KEY, API_SECRET)

def sumTransactions(account):
    transactions = account.get_transactions()
    transactionTotal = 0
    for trans in transactions.data:
        transactionTotal += float(trans.native_amount.amount)
    return transactionTotal

accounts = client.get_accounts()

@app.route("/")
def index():
    accountDict = {}
    for account in accounts.data:
        transactionSum = sumTransactions(account)
        profit = float(account.native_balance.amount) - transactionSum
        accountDict[str(account.balance.currency)] = {
            "nativeSpent": transactionSum,
            "nativeWorth": account.native_balance.amount,
            "profit": float(account.native_balance.amount) - transactionSum
        }
    return render_template("index.html", accountDict=accountDict)

if __name__ == "__main__":
    app.run(debug=True)