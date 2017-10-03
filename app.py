from coinbase.wallet.client import Client
import json

# Insert your API key and secret here
API_KEY = ""
API_SECRET = ""

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
print
for account in accounts.data:
    sums = sumTransactions(account)
    print "====== {} ======".format(account.balance.currency)
    print "Spent: {} {}".format(sums[0], sums[1])
    print "Worth: {} {}".format(account.native_balance.amount, account.native_balance.currency)
    print