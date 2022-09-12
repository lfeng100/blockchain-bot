import atexit
import slack
import os
import json
from bit import PrivateKeyTestnet

TEST = 0
CHANNEL = '#bot-test2' if TEST else '#blockchain-bot'

client = slack.WebClient(str(os.environ['SLACK_TOKEN']))
# client = slack.WebClient(str(os.getenv('SLACK_TOKEN')))

def show_all():
    client.chat_postMessage(channel=CHANNEL, text=f"*---USABLE WALLET INFO ON `btc-testnet`---*")
    f = open('btc-wallets.json')
    data = json.load(f)
    for wallet in data['btc_wallets']:
        client.chat_postMessage(channel=CHANNEL, text=f'----------------------')
        my_key = PrivateKeyTestnet(str(os.environ[wallet]))
        client.chat_postMessage(channel=CHANNEL, text=f"Wallet: `{wallet}`")
        client.chat_postMessage(channel=CHANNEL, text=f"BTC: `{my_key.get_balance('btc')}` (in USD: `{my_key.get_balance('usd')}`)")
    f.close()

def show_one(address):
    my_key = PrivateKeyTestnet(str(os.environ[address]))
    client.chat_postMessage(channel=CHANNEL, text=f"Wallet: `{address}`")
    client.chat_postMessage(channel=CHANNEL, text=f"BTC: `{my_key.get_balance('btc')}` (in USD: `{my_key.get_balance('usd')}`)")

def show_all_tokens():
    client.chat_postMessage(channel=CHANNEL, text=f"*---USABLE TOKEN INFO ON `btc-testnet`---*")
    client.chat_postMessage(channel=CHANNEL, text=f"Only `BTC` is available on this network")

def check_btc(token, address):
    if token != "btc":
        client.chat_postMessage(channel=CHANNEL, text=f"Note that only 'BTC' is available on this network")
    my_key = PrivateKeyTestnet(str(os.environ[address]))
    client.chat_postMessage(channel=CHANNEL, text=f"Wallet: `{address}` has BTC: `{my_key.get_balance('btc')}` (in USD: `{my_key.get_balance('usd')}`)")
