import time
from datetime import datetime

from rabbitx.payload import Payload


def test_payload_hash():
    data = dict(method='POST', path='/')
    current_timestamp = int(datetime.now().timestamp())
    p1 = Payload(current_timestamp, data)
    p2 = Payload(current_timestamp + 1, data)

    assert p1.hash != p2.hash

    data = dict(method='POST', path='/', hello='world')
    p3 = Payload(current_timestamp, data)

    assert p1.hash != p3.hash


def test_payload_sign_verify():
    secret = '0xdeadbeef'
    data = dict(method='POST', path='/')
    current_timestamp = int(datetime.now().timestamp())
    signature_lifetime = 1
    expired_timestamp = current_timestamp + signature_lifetime

    p = Payload(expired_timestamp, data)
    sig = p.sign(secret)
    assert p.verify(sig, secret)

    evil_sig = '0x734ac43bf06cd3ff9a3ed58e02b1350c23abcdc05629abff6c896d5a6f63c992'
    assert not p.verify(evil_sig, secret)

    time.sleep(signature_lifetime)
    assert not p.verify(evil_sig, secret)

    p.timestamp += 10
    assert not p.verify(sig, secret)