from rabbitx import const
from rabbitx.client.endpoints.order import OrderStatus
from rabbitx.client import Client
import os
from dotenv import load_dotenv
import argparse
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':

    # Set up argument parser
    parser = argparse.ArgumentParser(description='RabbitX API example')
    parser.add_argument('--testnet', action='store_true', help='Use testnet instead of mainnet')
    parser.add_argument('--exchange', type=str, default='rbx', choices=['rbx', 'bfx'], help='Choose the exchange: rbx (RabbitX) or bfx (Bitfinex)')
    args = parser.parse_args()

    # Use the parsed argument to set testnet
    testnet = args.testnet
    exchange = args.exchange

    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    public_jwt = os.environ['PUBLIC_JWT']
    private_jwt = os.environ['PRIVATE_JWT']

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

    def print_account_equity(client):
        account_info = client.account.get()
        print(f'\033[92m\nClient Account Equity:\n\033[0m', account_info['account_equity'])

    def test_deadman_switch(client):
        result = client.deadman.get(market_id=symbol)
        print(f'\033[92m\nDeadman switch status:\n\033[0m', result)

        result = client.deadman.remove(market_id=symbol)
        print(f'\033[92m\nDelete deadman return response:\n\033[0m', result)

        result = client.deadman.get(market_id=symbol)
        print(f'\033[92m\nDeadman switch status after delete:\n\033[0m', result)

        timeout_ms = 12000  # Set the timeout in milliseconds
        result = client.deadman.create(timeout=timeout_ms, market_id=symbol)
        print(f'\033[92m\n\n\nCancel all after {timeout_ms} ms result:\n\033[0m', result)

    # Onboarding is needed for private endpoints
    client.onboarding.init()
    
    # Print client account information
    print_account_equity(client)
    
    # Test the cancel_all_after endpoint
    test_deadman_switch(client)
    # client.deadman.remove()
