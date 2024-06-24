from datetime import datetime, timedelta

import jwt

from manager.models import Manager
from user.models import BlacklistedToken


def generate_token_jwt(user_id):
    payload = {
        'id': user_id,
        'exp': datetime.utcnow() + timedelta(days=50),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def check_token_manager(token):
    code = jwt.decode(token, 'manager_secret_key', algorithms='HS256')
    try:
        Manager.objects.get(id=int(code['id']))
        return int(code['id'])
    except:
        return -1


def checkToken(token):
    try:
        if BlacklistedToken.objects.filter(token=token).exists():
            return -1
        code = jwt.decode(token, 'secret', algorithms='HS256')
        return code['id']
    except:
        return -1
