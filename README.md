# L2F Blockchain Scripts
This repository holds scripts that easily allow for interaction with different blockchains through the command line.

## Chains

### Ethereum

1. Mainnet `mainnet`
1. Ropsten `ropsten`
1. Rinkeby `rinkeby`
1. Goerli `goerli`

### Avalanche

1. Mainnet `avax-main`
1. Testnet `avax-test`

### Polygon

1. Mainnet `polygon-main`
1. Testnet `polygon-test`

### Bitcoin
1. Bitcoin Testnet `btc-testnet`

## Setup
All interaction to the python brownie scripts are done through a rest-api to add an additional abstraction layer (makes it easier).

Before running locally, please visit the page above where details for local testing are in red text.

Ensure you have docker/docker-compose installed
1. build image `docker-compose build` (add option --no-cache if changes are made)
1. run image `docker-compose up`

Server should now be up and running and accepting requests. <br />
In the Slack api, Slack bot must be given chat:write and commands OAuth scopes and slash commands must be adde as specified in app.py (after each @app.route).

## Testing through Postman
If image is run locally, you can the hit address specified in the terminal (upon running docker-compose up) with the respective slash command being tested. The slash command is specified in the @app.route field in app.py. Create an HTTP Post request with the required parameters for the command (Make sure the Key is "text"):
![Postman Request](readme-images/postman.png?raw=true "Postman Request")
Notes: Change each instance of CHANNEL to a private channel is slack to avoid clogging up the main bot server. Make sure the bot is added as an App to the channel.

## Adding chain information

### Adding/change wallet
To add new wallets, add the private keys to the .env file inside the chain_interaction directory (do not use real wallets right now for security reasons). Then add the address to the brownie-config.yaml file (remove hex 0x start). This wallet should now be usable.

#### Adding private key image
![Adding private key](readme-images/private.png?raw=true "Adding private key")

#### Adding wallet image
![Adding new wallet](readme-images/wallet.png?raw=true "Adding wallet address")

### Adding/change coin info
To change/add token info depending on the chain, navigate to brownie-config.yaml and change or add new tokens with their corresponding contract address on that chain. You must also add the token contract ABI to the abi directory.

### Useful Documentation
brownie framework: https://eth-brownie.readthedocs.io/en/stable/ <br />
uniswap package: https://uniswap-python.com/getting-started.html#making-trades <br />
Infura with brownie: https://eth-brownie.readthedocs.io/en/v1.0.1/nonlocal-networks.html, https://docs.infura.io/infura/ <br />
