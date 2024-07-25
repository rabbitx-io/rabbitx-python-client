from dataclasses import dataclass

from rabbitx import const
from rabbitx.client.endpoint_group import EndpointGroup
from rabbitx.metamask import MetamaskSignRequest, metamask_sign
from rabbitx.util import hex2bytes


@dataclass
class APIKey:

    key: str
    secret: str


class OnboardingGroup(EndpointGroup):

    def onboarding(self):
        """
        Onboarding using private key
        """
        wallet = self.session.wallet
        signature = self._prepare_signature()
        data = dict(wallet=wallet, signature=signature, isClient=False)
        resp = self.session.session.post(
            f'{self.session.api_url}/onboarding',
            json=data,
            headers=self.session.headers,
        ).json()

        if resp['success'] != True:
            raise Exception(resp['error'])

        if resp['success']:
            api_secret = resp['result'][0]['apiSecret']
            self.session.api_key = api_secret['Key']
            self.session.api_secret = api_secret['Secret']
            self.session.public_jwt = resp['result'][0]['jwt']
            self.session.profile_id = resp['result'][0]['profile']['id']

        return resp['result'][0]

    def _prepare_signature(self) -> str:
        sign_request = MetamaskSignRequest(const.ONBOARDING_MESSAGE, self.session.expiration_timestamp)
        signature = metamask_sign(sign_request, self.session.private_key)
        signature = bytearray(hex2bytes(signature))
        signature[-1] = signature[-1] % 27

        return '0x' + signature.hex()

    def init(self):
        profile = self.session.profile.get()
        self.session.profile_id = profile['id']