
from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType, TimeInForce
from rabbitx.client import OrderStatus
import argparse
import json
import time
import os
from dotenv import load_dotenv
import json

os.chdir(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':

    # Set up argument parser
    parser = argparse.ArgumentParser(description='RabbitX API example')
    parser.add_argument('--testnet', action='store_true', help='Use testnet instead of mainnet')
    parser.add_argument('--exchange', type=str, default='rbx', choices=['rbx', 'bfx'], help='Choose the exchange: rbx (RabbitX) or bfx (Blast Futures Exchange)')
    args = parser.parse_args()

    # Use the parsed argument to set testnet
    testnet = args.testnet
    exchange = args.exchange

    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    
    # Read the apiKey.json exported from RabbitX during api key creation
    api_key_file = ''#'apiKey.json'
    if os.path.exists(api_key_file):
        with open(api_key_file, 'r') as file:
            api_data = json.load(file)
            # Extract the required information
            api_key = api_data['key']
            api_secret = api_data['secret']
            private_jwt = api_data['privateJwt']
            public_jwt = api_data['publicJwt']
            private_jwt = api_data['privateJwt']    
    else:
        # Load from .env environment variables if apiKey.json is not found
        api_key = os.environ.get('API_KEY')
        api_secret = os.environ.get('API_SECRET')
        public_jwt = os.environ.get('PUBLIC_JWT')
        private_jwt = os.environ.get('PRIVATE_JWT')

        if not all([api_key, api_secret, public_jwt, private_jwt]):
            print("Error: Required environment variables are not set.")
            exit(1)

    symbol = 'BTC-USD'
    
    if exchange == 'rbx':
        # Set up client
        if testnet:
            client = Client(api_url=const.TESTNET_URL, api_key=api_key, api_secret=api_secret,public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange) 
        else:
            client = Client(api_url=const.URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
    elif exchange == 'bfx':
        if testnet:
            client = Client(api_url=const.TESTNET_BFX_URL, api_key=api_key, api_secret=api_secret,public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)
        else:
            client = Client(api_url=const.BFX_URL, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt, private_jwt=private_jwt, exchange=exchange)

    # Onboarding is needed for private endpoints
    client.onboarding.init()
    # Get and print client profile information
    profile_info = client.profile.get()
    print('\033[92m\n\n\nClient Profile Information:\n\033[0m', json.dumps(profile_info, indent=4))
    # Get market information
    resp = client.markets.list([symbol])
    market = resp[0]
    print(f'\033[92m\n\n\n{symbol} market info:\n\033[0m', json.dumps(market, indent=4))

    while True:
        start_time = time.time()
        orders = client.orders.list(status=OrderStatus.OPEN)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to get orders: {elapsed_time} seconds")
    