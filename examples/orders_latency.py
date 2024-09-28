import time
import requests
import rabbitx
from rabbitx.client import Client
from rabbitx import const
import os
import json
from dotenv import load_dotenv
import argparse

load_dotenv('./.env') # create and change the .env-example file to .env and add your private key

api_key_file = 'apiKey.json' # exported from the rabbitx api dashboard
if os.path.exists(api_key_file):
    with open(api_key_file, 'r') as file:
        api_data = json.load(file)
        # Extract the required information
        api_key = api_data['key']
        api_secret = api_data['secret']
        private_jwt = api_data['privateJwt']
        public_jwt = api_data['publicJwt']
else:
    # Load from .env environment variables if apiKey.json is not found
    api_key = os.environ.get('API_KEY')
    api_secret = os.environ.get('API_SECRET')
    public_jwt = os.environ.get('PUBLIC_JWT')
    private_jwt = os.environ.get('PRIVATE_JWT')

    if not all([api_key, api_secret, public_jwt, private_jwt]):
        print("Error: Required environment variables are not set.")
        exit(1)

# Set up argument parser
parser = argparse.ArgumentParser(description='RabbitX API example')
parser.add_argument('--testnet', action='store_true', help='Use testnet instead of mainnet')
parser.add_argument('--exchange', type=str, default='rbx', choices=['rbx', 'bfx'], help='Choose the exchange: rbx (RabbitX) or bfx (Bitfinex)')
args = parser.parse_args()

# Use the parsed argument to set testnet
testnet = args.testnet
exchange = args.exchange

if exchange == 'rbx':
    # Set up client
    if testnet:
        client = Client(api_url=const.TESTNET_URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange) 
    else:
        client = Client(api_url=const.URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
elif exchange == 'bfx':
    if testnet:
        client = Client(api_url=const.TESTNET_BFX_URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
    else:
        client = Client(api_url=const.BFX_URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)

# Onboarding is needed for private endpoints
client.onboarding.init()

def measure_latency(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        latency = time.time() - start_time
        return response, latency
    return wrapper

@measure_latency
def place_limit_order(symbol, price, quantity):
    response = client.orders.create(
        market_id=symbol,
        price=price,
        side=rabbitx.client.OrderSide.LONG,
        size=quantity,
        type_=rabbitx.client.OrderType.LIMIT
    )
    return response

@measure_latency
def place_market_order(symbol, quantity):
    response = client.orders.create(
        market_id=symbol,
        side=rabbitx.client.OrderSide.LONG,
        price=1,
        size=quantity,
        type_=rabbitx.client.OrderType.MARKET
    )
    return response

@measure_latency
def cancel_order(order_id, symbol):
    response = client.orders.cancel(order_id=order_id, market_id=symbol)
    return response

@measure_latency
def place_limit_order_post_only(symbol, price, quantity):
    response = client.orders.create(
        market_id=symbol,
        price=price,
        side=rabbitx.client.OrderSide.LONG,
        size=quantity,
        type_=rabbitx.client.OrderType.LIMIT,
        time_in_force=rabbitx.client.TimeInForce.POSTONLY
    )
    return response

@measure_latency
def place_limit_order_ioc(symbol, price, quantity):
    response = client.orders.create(
        market_id=symbol,
        price=price,
        side=rabbitx.client.OrderSide.LONG,
        size=quantity,
        type_=rabbitx.client.OrderType.LIMIT,
        time_in_force=rabbitx.client.TimeInForce.IOC
    )
    return response

@measure_latency
def place_limit_order_fok(symbol, price, quantity):
    response = client.orders.create(
        market_id=symbol,
        price=price,
        side=rabbitx.client.OrderSide.LONG,
        size=quantity,
        type_=rabbitx.client.OrderType.LIMIT,
        time_in_force=rabbitx.client.TimeInForce.FOK
    )
    return response

@measure_latency
def set_stop_limit(symbol, stop_price, limit_price, quantity):
    response = client.orders.create(
        market_id=symbol,
        price=limit_price,
        side=rabbitx.client.OrderSide.LONG,
        size=quantity,
        type_=rabbitx.client.OrderType.STOP_LIMIT
    )
    return response

@measure_latency
def set_stop_market(symbol, stop_price, quantity):
    response = client.orders.create(
        market_id=symbol,
        price=1,  # Price is not needed for stop market orders
        side=rabbitx.client.OrderSide.LONG,
        size=quantity,
        type_=rabbitx.client.OrderType.STOP_MARKET
    )
    return response

import asyncio

async def main():
    # black listed = 3 seconds.
    # fok and ioc = 5 seconds.

    symbol = 'BTC-USD'
    price = 30000
    quantity = 0.01

    async def send_order(order_func, *args, **kwargs):
        response, latency = order_func(*args, **kwargs)  # Remove await here
        print(response)
        return latency, response

    tasks = []

    # Limit Order
    for _ in range(10):
        tasks.append(send_order(place_limit_order, symbol, price, quantity))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mLimit Order Latency: {latency:.4f}s\033[0m, Response: {response}")

    # Market Order
    tasks = []
    for _ in range(10):
        tasks.append(send_order(place_market_order, symbol, quantity))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mMarket Order Latency: {latency:.4f}s\033[0m, Response: {response}")

    # Cancel Order
    tasks = []
    for _, response in results:  # Unpack the tuple correctly
        order_id = response['id']
        tasks.append(send_order(cancel_order, order_id, symbol))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mCancel Order Latency: {latency:.4f}s\033[0m, Response: {response}")

    # Limit Order with Post Only
    tasks = []
    for _ in range(10):
        tasks.append(send_order(place_limit_order_post_only, symbol, price, quantity))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mLimit Order Post Only Latency: {latency:.4f}s\033[0m, Response: {response}")

    # Limit Order with Immediate or Cancel
    tasks = []
    for _ in range(10):
        tasks.append(send_order(place_limit_order_ioc, symbol, price, quantity))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mLimit Order IOC Latency: {latency:.4f}s\033[0m, Response: {response}")

    # Limit Order with Fill or Kill
    tasks = []
    for _ in range(10):
        tasks.append(send_order(place_limit_order_fok, symbol, price, quantity))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mLimit Order FOK Latency: {latency:.4f}s\033[0m, Response: {response}")

    # Set Stop Limit on Positions
    tasks = []
    for _ in range(10):
        tasks.append(send_order(set_stop_limit, symbol, stop_price=28000, limit_price=27950, quantity=quantity))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mSet Stop Limit Latency: {latency:.4f}s\033[0m, Response: {response}")

    # Set Stop Market on Positions
    tasks = []
    for _ in range(10):
        tasks.append(send_order(set_stop_market, symbol, stop_price=27500, quantity=quantity))
    results = await asyncio.gather(*tasks)
    for latency, response in results:
        print(f"\033[94mSet Stop Market Latency: {latency:.4f}s\033[0m, Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())
