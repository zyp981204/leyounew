from utils.zhenzismsclient import ZhenziSmsClient
import ssl
import json
ssl._create_default_https_context = ssl._create_unverified_context
import random

def get_verification_code(tel):
    """
    给用户发送验证码并返回该验证码
    :return: 发给用户的验证码
    """
    apiUrl = 'https://sms_developer.zhenzikj.com'  # 请求地址
    appId = '102573'  # 应用id
    appSecret = 'NTVlMTg2MmEtMjY3OC00MWIyLTljMTMtMzdlNGFhYmI1ZjUw'  # 应用密钥

    # 生成4位随机数验证码
    verification_code = ''
    for i in range(1,5):
        verification_code += str(random.randint(0,9))
    message = '您的乐游租车验证码为' + verification_code + '，有效时间为5分钟...'  # 短信内容
    messageId = 'leyou'  # 短信唯一标识

    client = ZhenziSmsClient(apiUrl, appId, appSecret)
    res = client.send(tel, message,messageId)

    res=json.loads(res)
    res["verification_code"]=verification_code
    return json.dumps(res)