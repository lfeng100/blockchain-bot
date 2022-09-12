# Script for getting/converting crypto

import slack
import atexit
import os
import sys
from brownie import accounts, config, network, Contract
from brownie.network import priority_fee
from scripts.helpers import get_account, get_token_contract, get_token_decimals, clean_up, convert_up, convert_down
from uniswap import Uniswap
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

atexit.register(clean_up)

# Constant gas
priority_fee("250 gwei")

TEST = 0
CHANNEL = '#bot-test2' if TEST else '#blockchain-bot'

client = slack.WebClient(str(os.environ['SLACK_TOKEN']))
# client = slack.WebClient(str(os.getenv('SLACK_TOKEN')))

def swap_erc20(amount, fromToken, toToken, receiver):
    account = receiver[2:]
    fromToken = f"{fromToken}_coin" if fromToken == "eth" else f"{fromToken}_token"
    toToken = f"{toToken}_coin" if toToken == "eth" else f"{toToken}_token"
    decimals = get_token_decimals(network.show_active(), fromToken)
    # print("Decimals: ", decimals, " Needed: ", convert_up(amount, decimals))
    # print(network.show_active())
    w3 = Web3(HTTPProvider(config["infura"].replace("network", network.show_active())))
    # middlware added for POA networks, see: http://web3py.readthedocs.io/en/stable/middleware.html#geth-style-proof-of-authority
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    uniswap_wrapper = Uniswap(address=receiver, private_key=config["wallets"][account], web3=w3, version=2)
    tx = uniswap_wrapper.make_trade(config[network.show_active()][fromToken]["contract"],
                                    config[network.show_active()][toToken]["contract"], convert_up(amount, decimals))


def check_eth(address, log=True):
    account = get_account(address)
    bal = account.balance()
    final_bal = convert_down(bal, 18)
    if log:
        msg = f'Wallet: `{address}` has ETH: `{final_bal}`'
        client.chat_postMessage(channel=CHANNEL, text=msg)
    return final_bal


def check_erc20(token, address, log=True):
    if token == "eth":
        return check_eth(address)

    account = get_account(address)
    tokenName = f"{token}_token"
    token_contract = get_token_contract(network.show_active(), tokenName)
    bal = token_contract.balanceOf(address)
    final_bal = convert_down(bal, get_token_decimals(network.show_active(), tokenName))
    if log:
        msg = f'Wallet: `{address}` has {token.upper()}: `{final_bal}`'
        client.chat_postMessage(channel=CHANNEL, text=msg)

    return final_bal


def show_all():
    client.chat_postMessage(channel=CHANNEL, text=f"*---USABLE WALLET INFO ON `{network.show_active()}`---*")
    for wallet in config["wallets"]:
        client.chat_postMessage(channel=CHANNEL, text=f'----------------------')
        wallet = f'0x{wallet}'
        client.chat_postMessage(channel=CHANNEL, text=f"Wallet: `{wallet}`")
        client.chat_postMessage(channel=CHANNEL, text=f"ETH: `{check_eth(wallet, False)}`")
        for token in config[network.show_active()]:
            if token != "eth_coin":
                token = token.replace("_token", "").replace("_coin", "")
                client.chat_postMessage(channel=CHANNEL, text=f"{token.upper()}: `{check_erc20(token, wallet, False)}`")

def show_one(address):
    if address[0:2] != "0x":
        address = "0x" + address
    client.chat_postMessage(channel=CHANNEL, text=f"Wallet: `{address}`")
    client.chat_postMessage(channel=CHANNEL, text=f"ETH: `{check_eth(address, False)}`")
    for token in config[network.show_active()]:
        if token != "eth_coin":
            token = token.replace("_token", "").replace("_coin", "")
            client.chat_postMessage(channel=CHANNEL, text=f"{token.upper()}: `{check_erc20(token, address, False)}`")


def show_all_tokens():
    client.chat_postMessage(channel=CHANNEL, text=f"*---USABLE TOKEN INFO ON `{network.show_active()}`---*")
    for token in config[network.show_active()]:
        token = token.replace("_token", "").replace("_coin", "")
        msg = f'Token: {token}'
        client.chat_postMessage(channel=CHANNEL, text=msg)
