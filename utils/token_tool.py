"""
    作者：詹亮   日期：2019/8/9 2:29 PM
"""

import jwt
from datetime import datetime,timedelta
# 私钥

SECRECT_KEY="2019-8-9"
EXPIRE=18000

def make_token(telephone,name=''):
    # 过期时间
    datetimeInt = datetime.utcnow() + timedelta(seconds=EXPIRE)

    # 载荷
    option = {
        "iss": "carbyleyou.com",
        "exp": datetimeInt,
        "iat": datetime.utcnow(),
        "aud": "webkit",
        "telephone": telephone,
        "name":name
    }
    # 构建令牌
    token = jwt.encode(option, SECRECT_KEY, 'HS256')

    return token

def check_token(token):
    telephone=None

    try:
        decoded = jwt.decode(token, SECRECT_KEY, audience='webkit', algorithms=['HS256'])
        telephone=decoded.get('telephone')

    except jwt.ExpiredSignatureError as ex:
        print(ex)
    except Exception as ex:
        print(ex)
    finally:
        return telephone