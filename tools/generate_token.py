from datetime import datetime, timedelta

import jwt

from user.models import BlacklistedToken


def generate_token_jwt(user_id):
    payload = {
        'id': user_id,
        'exp': datetime.utcnow() + timedelta(days=50),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def checkToken(token):
    try:
        if BlacklistedToken.objects.filter(token=token).exists():
            return -1
        code = jwt.decode(token, 'secret', algorithms='HS256')
        return code['id']
    except:
        return -1
