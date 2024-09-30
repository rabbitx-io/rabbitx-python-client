from rabbitx.client.endpoints.account import AccountGroup
from rabbitx.client.endpoints.candle import CandleGroup, CandlePeriod
from rabbitx.client.endpoints.fill import FillGroup
from rabbitx.client.endpoints.jwt import JWTGroup
from rabbitx.client.endpoints.market import MarketGroup
from rabbitx.client.endpoints.onboarding import OnboardingGroup, APIKey
from rabbitx.client.endpoints.order import OrderGroup, OrderSide, OrderType, OrderStatus, TimeInForce
from rabbitx.client.endpoints.orderbook import OrderBookGroup
from rabbitx.client.endpoints.position import PositionGroup
from rabbitx.client.endpoints.profile import ProfileGroup
from rabbitx.client.endpoints.balance import BalanceGroup
from rabbitx.client.endpoints.trade import TradeGroup
from rabbitx.client.endpoints.deadman import DeadmanGroup
from rabbitx.client.session import ClientSession
from rabbitx.client.websocket import WSClient, WSClientCallback


class Client(ClientSession):

    onboarding: OnboardingGroup
    orders: OrderGroup
    markets: MarketGroup
    candles: CandleGroup
    account: AccountGroup
    profile: ProfileGroup
    balance: BalanceGroup
    jwt: JWTGroup
    fills: FillGroup
    orderbook: OrderBookGroup
    trades: TradeGroup
    positions: PositionGroup

    def __init__(
        self,
        api_url: str,
        wallet: str = None,
        private_key: str = None,
        api_key: str = None,
        api_secret: str = None,
        public_jwt: str = None,
        private_jwt: str = None,
        exchange: str = None,
        debug: bool = False,
    ):
        super(Client, self).__init__(
            api_url,
            wallet,
            private_key,
            api_key,
            api_secret,
            public_jwt,
            private_jwt,
            exchange,
            debug,
        )

        self.onboarding = OnboardingGroup(self)
        self.orders = OrderGroup(self)
        self.markets = MarketGroup(self)
        self.candles = CandleGroup(self)
        self.account = AccountGroup(self)
        self.jwt = JWTGroup(self)
        self.fills = FillGroup(self)
        self.orderbook = OrderBookGroup(self)
        self.trades = TradeGroup(self)
        self.positions = PositionGroup(self)
        self.profile = ProfileGroup(self)
        self.balance = BalanceGroup(self)
        self.deadman = DeadmanGroup(self)
