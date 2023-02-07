from datetime import datetime
from web3.auto import w3

from rabbitx.metamask import metamask_sign, MetamaskSignRequest, metamask_verify, MetamaskVerifyRequest


def test_metamask_sign_verify():
    private_key = '0x0000000000000000000000000000000000000000000000000000000000000001'
    account = w3.eth.account.from_key(private_key)
    wallet = account.address
    message = 'Welcome to Rabbit DEX'

    signature_lifetime = 1
    current_timestamp = int(datetime.now().timestamp())
    expiration_timestamp = current_timestamp + signature_lifetime
    signature = metamask_sign(MetamaskSignRequest(message, expiration_timestamp), private_key)

    assert metamask_verify(MetamaskVerifyRequest(message, wallet, expiration_timestamp, signature))

    evil_signature = '0xf942293eff01d56e981e371e3943b6a13936ecc825deb8c5efc2e972c43de66d6267dcf342f955beac2700e1a476642a4815f804217691fd7eb92b43def1880000'
    assert not metamask_verify(MetamaskVerifyRequest(message, wallet, expiration_timestamp, evil_signature))
