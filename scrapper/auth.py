import jwt


def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, "secret", algorithm="HS256").decode("utf-8")
    return token


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, "secret", algorithms=["HS256"])
    return payload
