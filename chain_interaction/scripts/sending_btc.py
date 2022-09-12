import atexit
import slack
import os
from bit import PrivateKeyTestnet

TEST = 0
CHANNEL = '#bot-test2' if TEST else '#blockchain-bot'

client = slack.WebClient(str(os.environ['SLACK_TOKEN']))
# client = slack.WebClient(str(os.getenv('SLACK_TOKEN')))

def send_btc(amount, token, sender, receiver):
    if token == 'btc':
        my_key = PrivateKeyTestnet(str(os.environ[sender]))
        tx_hash = my_key.send([(receiver, amount, 'btc')])
        msg = f'Track transaction: https://blockchain.com/btc-testnet/tx/{tx_hash}'
        client.chat_postMessage(channel=CHANNEL, text=msg)
    else:
        client.chat_postMessage(channel=CHANNEL, text=f'Send Failed: Only BTC is available on this network --- Try Again!')
