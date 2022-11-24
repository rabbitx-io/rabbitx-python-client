def hex2bytes(value: str) -> bytes:
    if value.startswith('0x'):
        value = value[2:]

    return bytes.fromhex(value)
