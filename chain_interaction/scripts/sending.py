# Script for sending crypto from wallet to wallet

import atexit
import slack
import os
from brownie import accounts, config, network, Contract
from brownie.network import priority_fee
from scripts.helpers import get_account, get_token_contract, get_token_decimals, clean_up, convert_up, convert_down

atexit.register(clean_up)

# Constant gas
priority_fee("250 gwei")

TEST = 0
CHANNEL = '#bot-test2' if TEST else '#blockchain-bot'

client = slack.WebClient(str(os.environ['SLACK_TOKEN']))
# client = slack.WebClient(str(os.getenv('SLACK_TOKEN')))

def send_erc20(amount, token, sender, receiver):
    if token == "eth":
        send_eth(amount, sender, receiver)
    else:
        account = get_account(sender)
        token = f"{token}_token"
        token_contract = get_token_contract(network.show_active(), token)
        tx = token_contract.transfer(receiver, convert_up(amount, get_token_decimals(network.show_active(), token)),
                                     {"from": account, "required_confs": 0})
        msg = f'Track transaction: https://{network.show_active()}.etherscan.io/tx/{tx.txid}'
        client.chat_postMessage(channel=CHANNEL, text=msg)
        tx.wait(1)

def send_eth(amount, sender, receiver):
    account = get_account(sender)
    tx = account.transfer(receiver, f"{amount} ether")
    msg = f'Track transaction: https://{network.show_active()}.etherscan.io/tx/{tx.txid}'
    client.chat_postMessage(channel=CHANNEL, text=msg)
    tx.wait(1)

# def send_btc(amount, sender, receiver):
#     my_key = PrivateKeyTestnet(config["btc_wallets"][sender])
#     tx_hash = my_key.send([(receiver, amount, 'btc')])
#     msg = f'Track transaction: https://blockchain.com/btc-testnet/tx/{tx_hash}'
#     client.chat_postMessage(channel=CHANNEL, text=msg)
