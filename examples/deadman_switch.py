from rabbitx import const
from rabbitx.client.endpoints.order import OrderStatus
from rabbitx.client import Client
import os
from dotenv import load_dotenv

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    load_dotenv('./.env') # create and change the .env-example file to .env and add your private key
    private_jwt = os.environ['PRIVATE_JWT']
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    public_jwt = os.environ['PUBLIC_JWT']
    wallet = os.environ['WALLET']
    testnet=False # change this to True if using on testnet
    
    # Set up client
    if testnet:
        client = Client(api_url=const.TESTNET_URL, wallet=wallet, private_jwt=private_jwt, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt) 
    else:
        client = Client(api_url=const.URL, wallet=wallet, private_jwt=private_jwt, api_key=api_key, api_secret=api_secret, public_jwt=public_jwt)

    # Onboarding is needed for private endpoints
    client.onboarding.init()
    # Print client account information
    account_info = client.account.get()
    print(f'\033[92m\nClient Account Equity:\n\033[0m', account_info['account_equity'])
    # Print client open orders count
    open_orders = client.orders.list(status=OrderStatus.OPEN)
    print(f'\033[92m\nClient Open Orders Count:\n\033[0m', len(open_orders))
    # Test the cancel_all_after endpoint
    result = client.orders.get_cancel_all_after()
    print(f'\033[92m\nDeadman switch status:\n\033[0m', result)
    result = client.orders.delete_cancel_all_after()
    print(f'\033[92m\nDelete cancel all after result:\n\033[0m', result)
    timeout_ms = 5000  # Set the timeout in milliseconds
    result = client.orders.cancel_all_after(timeout_ms)
    print(f'\033[92m\n\n\nCancel all after {timeout_ms} ms result:\n\033[0m', result)
    # Test the get_deadman_switch endpoint
    