from rabbitx import const
from rabbitx.client import Client, CandlePeriod, OrderSide, OrderType

if __name__ == '__main__':
    private_key = '0x0000000000000000000000000000000000000000000000000000000001221104'
    symbol = 'BTC-USD'
    client = Client(api_url=const.DEV_URL, private_key=private_key)

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
        0.001,
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

    # orders = client.orders.list(market_id=symbol)
    # print('\n\n\nget order list:\n', orders)

    account = client.account.get()
    print('\n\n\naccount:\n', account)

    # check jwt is valid or not (for stage env)
    client.account.validate(client._jwt)

    new_leverage = client.account.set_leverage('BTC-USD', 10)
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

    # fills = client.fills.list(
    #     client.current_timestamp - 10,
    #     client.current_timestamp + 10,
    #     0,
    #     100,
    #     ['BTC-USD', 'SOL-USD'],
    # )
    # print('\n\n\nfills:\n', fills)
