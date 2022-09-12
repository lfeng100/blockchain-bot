# Setup
FROM python:3.8-slim-buster
WORKDIR /blockchain
COPY . .

RUN apt update
RUN apt -y install build-essential
RUN apt-get install -y git
RUN pip install -r requirements.txt
RUN pip install pipx
RUN pip install eth-brownie
RUN pip install bit
RUN pipx ensurepath
RUN pipx install eth-brownie
RUN pipx inject eth-brownie git+https://github.com/uniswap-python/uniswap-python
RUN pipx inject eth-brownie slack
RUN pipx inject eth-brownie slackclient
RUN pipx ensurepath

ENV FLASK_APP=slack-bot/app.py
ENTRYPOINT python -m flask run --host=0.0.0.0 --port=8080
