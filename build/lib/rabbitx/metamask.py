from dataclasses import dataclass
from datetime import datetime

from eth_account.messages import encode_defunct
from hexbytes import HexBytes
from web3.auto import w3

from rabbitx.util import hex2bytes


@dataclass
class MetamaskSignRequest:

    message: str
    timestamp: int


@dataclass
class MetamaskVerifyRequest:

    message: str
    wallet: str
    timestamp: int
    signature: str


def metamask_sign(request: MetamaskSignRequest, private_key: str):
    private_key = hex2bytes(private_key)
    metamask_message = f'{request.message}\n{request.timestamp}'
    message = encode_defunct(metamask_message.encode())
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)

    return signed_message.signature.hex()


def metamask_verify(request: MetamaskVerifyRequest) -> bool:
    metamask_message = f'{request.message}\n{request.timestamp}'
    message = encode_defunct(metamask_message.encode())
    signature = HexBytes(hex2bytes(request.signature))
    recovered_wallet = w3.eth.account.recover_message(message, signature=signature)

    if recovered_wallet.lower() != request.wallet.lower():
        return False

    current_timestamp = int(datetime.now().timestamp())

    if current_timestamp >= request.timestamp:
        return False

    return True
