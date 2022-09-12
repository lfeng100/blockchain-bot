# Script with helpful functions

import json
import shutil
from brownie import accounts, config, Contract

def get_account(account):
    account = account[2:]
    return accounts.add(config["wallets"][account])


def get_token_contract(chain_network, token):
    contract_address = config[chain_network][token]["contract"]

    f = open(f'abi/{token}.json')
    abi = json.loads(f.read())
    f.close()

    return Contract.from_abi("Token", contract_address, abi)


def get_token_decimals(chain_network, token):
    return config[chain_network][token]["decimals"]


def get_contract(chain_network, contract):
    contract_address = config[chain_network][contract]

    f = open(f'abi/{contract}.json')
    abi = json.loads(f.read())
    f.close()

    return Contract.from_abi("Contract", contract_address, abi)


def convert_up(amount, digits):
    return int(float(amount) * 10 ** digits)


def convert_down(amount, digits):
    return float(int(amount) / 10 ** digits)


def clean_up():
    shutil.rmtree('scripts/contracts')
    shutil.rmtree('scripts/deployments')
    shutil.rmtree('scripts/interfaces')
