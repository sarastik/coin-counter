from coinbase.wallet.client import Client
from api_keys import *
import json

client = Client(API_KEY, API_SECRET)

def sumTransactions(account):
    transactions = account.get_transactions()
    native_total = 0
    native_currency = ""
    for trans in transactions.data:
        native_total += float(trans.native_amount.amount)
        native_currency = trans.native_amount.currency
    return (native_total, native_currency)

accounts = client.get_accounts()

for account in accounts.data:
    nativeSum = sumTransactions(account)
    profit = float(account.native_balance.amount) - nativeSum[0]

    print "========= {} =========".format(account.balance.currency)
    print "Spent: {} {}".format(nativeSum[0], nativeSum[1])
    print "Worth: {} {}".format(account.native_balance.amount, account.native_balance.currency)
    print "You've {} {} {}".format(("earned" if profit > 0 else "lost"), abs(profit), account.native_balance.currency)
    print