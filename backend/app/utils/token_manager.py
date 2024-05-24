import hmac
import hashlib
import datetime
from urllib.request import Request

from fastapi import HTTPException


def verify_token(userId, token):
    if userId is None or token is None:
        return False
    # 解析token，获取过期时间
    expire_time_str = token.split(".")[0]

    hmacToken = token.split(".")[1]

    payload = {
        'user_id': userId,
        'expire_time': expire_time_str
    }

    # 验证token是否被篡改
    newToken = hmac.new(SECRET_KEY, str(payload).encode('utf-8'), hashlib.sha256).hexdigest()
    if newToken != hmacToken:
        return False

    # 检查是否过期，考虑系统时间和接口传来时间相差不超过2分钟
    now_time = datetime.datetime.now()
    expire_time = datetime.datetime.strptime(expire_time_str, '%Y-%m-%d %H:%M:%S')
    time_difference = now_time - expire_time
    if abs(time_difference.total_seconds()) > 60:
        return False

    return True


def validate_signature(request: Request):
    # 获取请求参数
    header_params = dict(request.headers)

    if verify_token(header_params.get("user_id"), header_params.get("token")) is False:
        raise HTTPException(status_code=401, detail="user_token is invalid")

    # 过滤header_params，只取nonce、timestamp、token
    pre_header_params = {k: v for k, v in header_params.items() if k in ('nonce', 'timestamp', 'token', "user_id")}

    pre_header_params = {**request.query_params, **pre_header_params}

    # 将请求参数按升序行排序
    sorted_params = sorted(pre_header_params.items())

    # 排序之后拼接成一个字符串
    param_str = "&".join(f"{k}={v}" for k, v in sorted_params)
    print(param_str)

    # 使用公钥（secretkey）对拼接后的字符串生成签名
    expected_sign = hmac.new(SECRET_KEY, param_str.encode("utf-8"), hashlib.sha256).hexdigest().lower()
    print(expected_sign)
    print(header_params.get('sign'))
    # 比较请求中的sign和期望的sign
    if header_params.get('sign') != expected_sign:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return True


def generate_token(user_id):
    now = datetime.datetime.now()
    expire_time = now + datetime.timedelta(days=1)
    payload = {
        'user_id': user_id,
        'expire_time': expire_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    token = str(payload["expire_time"]) + "." + hmac.new(SECRET_KEY, str(payload).encode('utf-8'),
                                                         hashlib.sha256).hexdigest()
    return token


# 示例密钥，实际应用中应该使用安全的方式保存密钥
SECRET_KEY = b'aad3411d6be8cd1da118fd5130636276'

# # 创建TokenManager实例
# token_manager = TokenManager()
#
# # 示例用户ID
# user_id = '5356221715'
#
# # 生成token
# token = token_manager.generate_token(user_id)
# print("生成的token:", token)
#
# # 验证token是否过期
# is_expired = token_manager.verify_token(user_id, token)
# print("Token是否通过:", is_expired)
