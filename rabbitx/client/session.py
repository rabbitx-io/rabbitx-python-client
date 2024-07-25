from datetime import datetime
from typing import Any

import requests
from requests import Session
from web3.auto import w3
from eth_account.signers.local import LocalAccount
from ulid import ULID

from rabbitx import const
from rabbitx.payload import Payload


class ClientSession:

    session: Session
    api_url: str
    _wallet: str
    private_key: str
    api_key: str
    api_secret: str
    public_jwt: str
    _current_timestamp: int
    _signature: str
    profile_id: int
    exchange: str

    def __init__(
        self,
        api_url: str,
        wallet: str = None,
        private_key: str = None,
        api_key: str = None,
        api_secret: str = None,
        public_jwt: str = None,
        private_jwt: str = None,
        exchange: str = 'rbx',
    ):
        self.session = requests.Session()
        self.api_url = api_url.rstrip('/')
        self._wallet = wallet
        self.private_key = private_key
        self.api_key = api_key
        self.api_secret = api_secret
        self.public_jwt = public_jwt
        self.private_jwt = private_jwt
        self._current_timestamp = 0
        self._signature = ''
        self.exchange = exchange
        original_post = self.session.post
        original_get = self.session.get
        original_put = self.session.put
        original_delete = self.session.delete


        def patched_post(*args, **kwargs):
            result = original_post(*args, **kwargs)
            self._current_timestamp = 0
            self._signature = ''
            return result

        def patched_get(*args, **kwargs):
            result = original_get(*args, **kwargs)
            self._current_timestamp = 0
            self._signature = ''
            return result

        def patched_put(*args, **kwargs):
            result = original_put(*args, **kwargs)
            self._current_timestamp = 0
            self._signature = ''
            return result

        def patched_delete(*args, **kwargs):
            result = original_delete(*args, **kwargs)
            self._current_timestamp = 0
            self._signature = ''
            return result

        self.session.post = patched_post
        self.session.get = patched_get
        self.session.put = patched_put
        self.session.delete = patched_delete

    @property
    def current_timestamp(self) -> int:
        if self._current_timestamp == 0:
            self._current_timestamp = int(datetime.now().timestamp())

        return self._current_timestamp

    @property
    def expiration_timestamp(self) -> int:
        return self.current_timestamp + const.SIGNATURE_LIFETIME

    @property
    def headers(self) -> dict[str, str]:
        headers = {'RBT-TS': str(self.expiration_timestamp)}
        headers['Request-ID'] = str(ULID())

        if self.api_key:
            headers['RBT-API-KEY'] = self.api_key

        if self._signature:
            headers['RBT-SIGNATURE'] = self._signature
        if self.exchange != 'rbx':
            headers['EID'] = self.exchange

        return headers

    @property
    def wallet(self) -> str:
        if self._wallet:
            return self._wallet

        if not self.private_key:
            raise ValueError

        account: LocalAccount = w3.eth.account.from_key(self.private_key)
        
        return account.address

    def sign_request(self, data: dict[str, Any]):
        payload = Payload(self.expiration_timestamp, data)
        if not self.api_secret:
            raise ValueError('Unauthorised, check your api key and secret or use client.onboarding.onboarding() to authorise.')
        self._signature = payload.sign(self.api_secret)
