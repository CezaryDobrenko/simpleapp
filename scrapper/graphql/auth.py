import time
from functools import wraps

from scrapper.models.api_key import ApiKey
from scrapper.models.user import User


def get_authorization(context):
    try:
        return context.environ["HTTP_AUTHORIZATION"]
    except:
        try:
            return context["request"].headers["Authorization"]
        except:
            raise Exception("Invalid request")


def get_user_from_api_token(api_token: str) -> User:
    key = ApiKey.objects.filter(key=api_token).first()
    if key:
        if key.is_active:
            if time.time() < key.expired_at.timestamp():
                return key.user
            else:
                raise Exception("Api key is expired!")
        else:
            raise Exception("Api key is inactive!")
    else:
        raise Exception("Invalid api key!")


def authenticate_required():
    def decorator(func):
        @wraps(func)
        def wrapper(root, info, *args, **kwargs):
            authorization = get_authorization(info.context)
            api_token = "".join(authorization.split())[6:]
            kwargs["api_token"] = api_token
            kwargs["current_user"] = get_user_from_api_token(api_token)
            return func(root, info, *args, **kwargs)

        return wrapper

    return decorator
