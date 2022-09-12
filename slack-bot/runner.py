import subprocess
import uuid

TEST = 0
CHANNEL = '#bot-test2' if TEST else '#blockchain-bot'

def run_script(client, command):
    request_id = str(uuid.uuid4())
    # client.chat_postMessage(channel=CHANNEL, text=f'Starting... request_id: `{request_id}`')
    try:
        subprocess.check_output(command, shell=True)
        client.chat_postMessage(channel=CHANNEL, text=f'🟢 Command executed successfully.')
    except subprocess.CalledProcessError as e:
        output = str(e.output)
        # client.chat_postMessage(channel=CHANNEL, text=output)
        if "config[\"wallets\"][account]" in output:
            client.chat_postMessage(channel=CHANNEL, text=f'❌ Error executing command: Check if the wallet entered is valid (To add a wallet, see blockchain-scripts repo)')
        elif ("Gas estimation failed" in output) or ("InsufficientBalance" in output):
            client.chat_postMessage(channel=CHANNEL, text=f'❌ Error executing command: There were insufficient funds to complete the transfer')
        elif "config[chain_network][token]" in output:
            client.chat_postMessage(channel=CHANNEL, text=f'❌ Error executing command: Check if the token/coin entered is valid')
        elif "[toToken]" in output:
            client.chat_postMessage(channel=CHANNEL, text=f'❌ Error executing command: Check if the token/coin entered is valid')
        else:
            client.chat_postMessage(channel=CHANNEL, text=f'❌ Error executing command: Type /blockchain_help for tips on command usage and available networks')
    # status = '*Failed* ❌' if rc else '*Success* 🟢'
    # client.chat_postMessage(channel=CHANNEL, text=f'Finished request_id: `{request_id}` with status: {status}')

    client.chat_postMessage(channel=CHANNEL, text=f'__________________________________________________')
