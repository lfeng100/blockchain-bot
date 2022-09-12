import slack
import os
import pathlib
import json
from pathlib import Path
from threading import Thread
from flask import Flask, request, Response
from dotenv import load_dotenv
from runner import run_script

env_path = Path('.') / 'chain_interaction/.env'

load_dotenv(dotenv_path=env_path)

with open("chain_interaction/.env", "r+") as text_file:
    texts = text_file.read()
    texts = texts.replace("walletKey1", (str(os.environ['PRIVATE_KEY_1'])))
    texts = texts.replace("walletKey2", (str(os.environ['PRIVATE_KEY_2'])))
    texts = texts.replace("walletKey3", (str(os.environ['PRIVATE_KEY_3'])))
    texts = texts.replace("btcWalletKey1", (str(os.environ['mmJYyLNUr62aR3baDcNSY5aRVyC9tGSsF6'])))
    texts = texts.replace("btcWalletKey2", (str(os.environ['n1XtWd1TTFEXaBW2mepDHxUy1D8m1gGvzk'])))
    texts = texts.replace("infuraID", (str(os.environ['WEB3_INFURA_PROJECT_ID'])))
    texts = texts.replace("infuraURL", (str(os.environ['WEB3_INFURA_PROJECT_URL'])))
    texts = texts.replace("slackToken", (str(os.environ['SLACK_TOKEN'])))

with open("chain_interaction/.env", "w") as text_file:
    text_file.write(texts)

TEST = 0
CHANNEL = '#bot-test2' if TEST else '#blockchain-bot'
SUCCESSFUL_RESPONSE = 'Request successfully submitted.'
ERROR_RESPONSE = 'Request failure, please verify entered command.'
networks = ['ropsten', 'rinkeby', 'mainnet', 'goerli', 'btc-testnet']
commandDescriptions = ["/blockchain-info [network]\n     i.e. /blockchain-info ropsten ---- Shows usable wallets on ropsten network and their respective balances\n\n",
                        "/blockchain-wallet-info [wallet network]\n     i.e. /blockchain-wallet-info 0xABCD1234 ropsten ---- Shows balances of 0xABCD1234 on ropsten network\n\n",
                        "/blockchain-token-info [network]\n     i.e. /blockchain-token-info ropsten ---- Shows usable coins on ropsten network\n\n",
                        "/blockchain-check [asset wallet network]\n     i.e. /blockchain-check USDC 0xABCD1234 ropsten ---- Checks the amount of USDC in wallet 0xABCD1234 on ropsten network\n\n",
                        "/blockchain-swap [amount fromAsset toAsset wallet network]\n     i.e. /blockchain-swap 5 USDC ETH 0xABCD1234 ropsten ---- Swaps 5 USDC for ETH in wallet 0xABCD1234 on ropsten network\n\n",
                        "/blockchain-send [amount asset senderWallet receiverWallet network]\n     i.e. /blockchain-send 0.05 eth 0xABCD1234 0xWXYZ6789 ropsten ---- Sends 0.05 ETH from 0xABCD1234 to 0xWXYZ6789 on ropsten network\n\n"]

app = Flask(__name__)

# from .env file
client = slack.WebClient(str(os.environ['SLACK_TOKEN']))
# client = slack.WebClient(str(os.getenv('SLACK_TOKEN')))

@app.route('/blockchain-info', methods=['POST'])
def blockchain_info():
    params = request.form.get('text')
    params = params.lower()
    client.chat_postMessage(channel=CHANNEL, text=f"Command executed: `/blockchain-info {params}`")
    split = params.split(' ')

    # error if less than required parameters
    if not params or len(split) < 1:
        client.chat_postMessage(channel=CHANNEL, text=f"Command Usage:\n" + commandDescriptions[0] + "__________________________________________________")
        return app.response_class(response=json.dumps(ERROR_RESPONSE), status=400, mimetype='application/json')

    run = f"Checking usable wallets on `{split[0]}`."
    client.chat_postMessage(channel=CHANNEL, text=run)

    thread = Thread(target=run_script, args=(client, f"/bin/bash run.sh show all {params}"))
    thread.start()
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

@app.route('/blockchain-wallet-info', methods=['POST'])
def blockchain_wallet_info():
    params = request.form.get('text')
    client.chat_postMessage(channel=CHANNEL, text=f"Command executed: `/blockchain-wallet-info {params}`")
    split = params.split(' ')

    if not params or len(split) < 2:
        client.chat_postMessage(channel=CHANNEL, text=f"Command Usage:\n" + commandDescriptions[1] + "__________________________________________________")
        return app.response_class(response=json.dumps(ERROR_RESPONSE), status=400, mimetype='application/json')

    run = f"Checking balances of `{split[0]}` on `{split[1]}`."
    client.chat_postMessage(channel=CHANNEL, text=run)

    thread = Thread(target=run_script, args=(client, f"/bin/bash run.sh show one {params}"))
    thread.start()
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

@app.route('/blockchain-token-info', methods=['POST'])
def blockchain_token_info():
    params = request.form.get('text')
    client.chat_postMessage(channel=CHANNEL, text=f"Command executed: `/blockchain-token-info {params}`")
    split = params.split(' ')
    if not params or len(split) < 1:
        client.chat_postMessage(channel=CHANNEL, text=f"Command Usage:\n" + commandDescriptions[2] + "__________________________________________________")
        return app.response_class(response=json.dumps(ERROR_RESPONSE), status=400, mimetype='application/json')

    run = f"Checking usable tokens on `{split[0]}`."

    client.chat_postMessage(channel=CHANNEL, text=run)

    thread = Thread(target=run_script, args=(client, f"/bin/bash run.sh token-show {params}"))
    thread.start()
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

@app.route('/blockchain-check', methods=['POST'])
def blockchain_check():
    params = request.form.get('text')
    client.chat_postMessage(channel=CHANNEL, text=f"Command executed: `/blockchain-check {params}`")
    split = params.split(' ')

    if not params or len(split) < 3:
        client.chat_postMessage(channel=CHANNEL, text=f"Command Usage:\n" + commandDescriptions[3] + "__________________________________________________")
        return app.response_class(response=json.dumps(ERROR_RESPONSE), status=400, mimetype='application/json')

    # change currency names to lower case:
    params = split[0].lower() + ' ' + split[1] +  ' ' + split[2]

    run = f"Checking specific asset `{split[0].upper()}` for wallet `{split[1]}` on `{split[2]}`."
    client.chat_postMessage(channel=CHANNEL, text=run)
    thread = Thread(target=run_script, args=(client, f"/bin/bash run.sh check {params}"))
    thread.start()
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

@app.route('/blockchain-swap', methods=['POST'])
def blockchain_swap():
    params = request.form.get('text')
    client.chat_postMessage(channel=CHANNEL, text=f"Command executed: `/blockchain-swap {params}`")
    split = params.split(' ')

    if not params or len(split) < 5:
        client.chat_postMessage(channel=CHANNEL, text=f"Command Usage:\n" + commandDescriptions[4] + "__________________________________________________")
        return app.response_class(response=json.dumps(ERROR_RESPONSE), status=400, mimetype='application/json')
    elif split[1].lower() == 'btc' or split[2].lower() == 'btc':
        client.chat_postMessage(channel=CHANNEL, text=f"Swapping is not supported with `BTC` \n__________________________________________________")
        return app.response_class(response=json.dumps(ERROR_RESPONSE), status=400, mimetype='application/json')
    # change currency names to lower case:
    params = split[0] + ' ' + split[1].lower() +  ' ' + split[2].lower() +  ' ' + split[3] +  ' ' + split[4]


    run = f"Will be swapping `{split[0]} {split[1].upper()}` for `{split[2].upper()}` from `{split[3]}` on `{split[4]}`."
    client.chat_postMessage(channel=CHANNEL, text=run)
    thread = Thread(target=run_script, args=(client, f"/bin/bash run.sh swap {params}"))
    thread.start()
    client.chat_postMessage(channel=CHANNEL, text=f"Balances may take some time to reflect")
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

@app.route('/blockchain-send', methods=['POST'])
def blockchain_send():
    params = request.form.get('text')
    client.chat_postMessage(channel=CHANNEL, text=f"Command executed: `/blockchain-send {params}`")
    split = params.split(' ')


    if not params or len(split) < 5:
        client.chat_postMessage(channel=CHANNEL, text=f"Command Usage:\n" + commandDescriptions[5] + "__________________________________________________")
        return app.response_class(response=json.dumps(ERROR_RESPONSE), status=400, mimetype='application/json')

    # change currency names to lower case:
    params = split[0] + ' ' + split[1].lower() +  ' ' + split[2] +  ' ' + split[3] +  ' ' + split[4]

    run = f"Will be sending `{split[0]} {split[1].upper()}` from `{split[2]}` to `{split[3]}` on `{split[4]}`."
    client.chat_postMessage(channel=CHANNEL, text=run)
    client.chat_postMessage(channel=CHANNEL, text="Processing... This may take a moment")
    thread = Thread(target=run_script, args=(client, f"/bin/bash run.sh send {params}"))
    thread.start()
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

@app.route('/blockchain-help', methods=['POST'])
def blockchain_help():
    client.chat_postMessage(channel=CHANNEL, text=f"Command executed: `/blockchain-help`")
    client.chat_postMessage(channel=CHANNEL, text=f"*Current Available Networks:*")
    for network in networks:
        client.chat_postMessage(channel=CHANNEL, text=network)

    client.chat_postMessage(channel=CHANNEL, text=f"*Blockchain Bot Commands:*")
    client.chat_postMessage(channel=CHANNEL, text=f"Note: /blockchain-swap does not work on btc-testnet")
    for description in commandDescriptions:
        client.chat_postMessage(channel=CHANNEL, text=description)
    client.chat_postMessage(channel=CHANNEL, text=f'__________________________________________________')
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

@app.route('/healthz', methods=['GET'])
def blockchain_health_check():
    return app.response_class(response=json.dumps(SUCCESSFUL_RESPONSE), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=False, port=8080)
