from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType

if __name__ == '__main__':
    private_key = '0x0000000000000000000000000000000000000000000000000000000011221104'
    symbol = 'BTC-USD'
    client = Client(api_url=const.TESTNET_URL, private_key=private_key)

    resp = client.markets.list([symbol])
    market = resp[0]
    print(f'{symbol} market info:\n', market)

    orderbook = client.orderbook.get('BTC-USD')[0]
    print(f'{symbol} orderbook:\n', orderbook)

    client.onboarding.onboarding()
    
    order_1 = client.orders.create(
        'BTC-USD',
        float(market['index_price']),
        OrderSide.LONG,
        0.002,
        OrderType.LIMIT,
    )
    print('\n\n\norder creation:\n', order_1)

    order_2 = client.orders.create(
        'BTC-USD',
        float(market['index_price']),
        OrderSide.SHORT,
        0.001,
        OrderType.LIMIT,
    )

    
    client.orders.amend(order_1['id'], symbol, float(market['index_price'])-1, 2)
    client.orders.cancel(order_1['id'], symbol)
    
    orders = client.orders.list(None, 'open')
    print('\n\n\nopen order list:\n', orders)

    account = client.account.get()
    print('\n\n\naccount:\n', account)
    
    # check jwt is valid or not (for stage env)
    client.account.validate(client._jwt)

    new_leverage = client.account.set_leverage('BTC-USD', 20)
    print('\n\n\nnew leverage:\n', new_leverage)

    candles = client.candles.list(
        'BTC-USD',
        client.current_timestamp - 10,
        client.current_timestamp + 10,
        CandlePeriod.M1,
    )
    print('\n\n\ncandles:\n', candles)

    new_jwt = client.jwt.update()
    print('\n\n\nnew jwt:\n', candles)

    fills = client.fills.list()
    print('\n\n\nfills:\n', fills)

    # order_fills = client.fills.list_by_order(order_id=order_1['id'])
    # print('\n\n\norder fills:\n', order_fills)