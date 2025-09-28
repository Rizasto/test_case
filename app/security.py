from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError

from app.user_data.user_data_service import UserAction
from config import JWT_SETTINGS

AUTH_SECRET = JWT_SETTINGS['auth_secret']
ACCESS_TTL_MIN = JWT_SETTINGS['access_ttl_min']
ALGO = JWT_SETTINGS['algo']
bearer = HTTPBearer(auto_error=False)
revoked_access: dict[str, int] = {}


def issue_access(user_id: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        'sub': str(user_id),
        'jti': str(uuid4()),
        'iat': now,
        'nbf': now,
        'exp': now + timedelta(minutes=int(ACCESS_TTL_MIN))
    }
    return jwt.encode(payload, AUTH_SECRET, algorithm=ALGO)


def get_bearer_token(creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer)) -> str:
    if creds is None:
        raise HTTPException(status_code=401, detail='Missing Authorization header')
    if (creds.scheme or '').lower() != 'bearer':
        raise HTTPException(status_code=401, detail='Invalid auth scheme')
    token = (creds.credentials or '').strip()
    if not token:
        raise HTTPException(status_code=401, detail='Empty bearer token')
    return token


def decode_access(token: str) -> dict:
    token = token.strip()
    try:
        payload = jwt.decode(
            token,
            AUTH_SECRET,
            algorithms=[ALGO],
            options={'require': ['sub', 'exp', 'iat', 'jti']},
            leeway=10
        )
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')

    jti = payload.get('jti')
    now_ts = int(datetime.now(timezone.utc).timestamp())
    _gc_revoked(now_ts)
    if jti in revoked_access and revoked_access[jti] > now_ts:
        raise HTTPException(status_code=401, detail='Token revoked')

    return payload


def get_current_user(token: str = Depends(get_bearer_token)):
    payload = decode_access(token)
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail='Invalid token payload (no sub)')
    user = UserAction().get_user_by_id(user_id)
    if not user or not getattr(user, 'is_active', False):
        raise HTTPException(status_code=401, detail='Unauthorized')
    return user


def _gc_revoked(now_ts: int):
    kill = [j for j, exp in revoked_access.items() if exp <= now_ts]
    for j in kill:
        revoked_access.pop(j, None)

