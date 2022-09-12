#!/bin/bash
# Script to perform blockchain interactions

if [ "$1" == "swap" ]; then # $2-amount $3-fromAsset $4-toAsset $5-wallet $6-network
    # Peform swap
    cd chain_interaction
    brownie run scripts/receiving.py swap_erc20 "$2" "$3" "$4" "$5" --network "$6"
elif [ "$1" == "send" ]; then
    # Perform send
    cd chain_interaction
    if [ "$6" == "btc-testnet" ]; then
      python -c "from scripts.sending_btc import send_btc; send_btc('$2', '$3', '$4', '$5')"
    else
      brownie run scripts/sending.py send_erc20 "$2" "$3" "$4" "$5" --network "$6"
    fi
elif [ "$1" == "check" ]; then
    cd chain_interaction
    if [ "$4" == "btc-testnet" ]; then
      python -c "from scripts.receiving_btc import check_btc; check_btc('$2', '$3')"
    else
      brownie run scripts/receiving.py check_erc20 "$2" "$3" --network "$4"
    fi
elif [ "$1" == "show" ]; then
    cd chain_interaction
    if [ "$2" == "all" ]; then
      if [ "$3" == "btc-testnet" ]; then
        python -c "from scripts.receiving_btc import show_all; show_all()"
      else
        brownie run scripts/receiving.py show_all --network "$3"
      fi
    else
      if [ "$4" == "btc-testnet" ]; then
        python -c "from scripts.receiving_btc import show_one; show_one('$3')"
      else
        brownie run scripts/receiving.py show_one "$3" --network "$4"
      fi
    fi
elif [ "$1" == "token-show" ]; then
    cd chain_interaction
    if [ "$2" == "btc-testnet" ]; then
      python -c "from scripts.receiving_btc import show_all_tokens; show_all_tokens()"
    else
      brownie run scripts/receiving.py show_all_tokens --network "$2"
    fi
else
    echo "Error: Run command not recognized"
fi
