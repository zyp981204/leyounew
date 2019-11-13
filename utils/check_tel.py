"""
作者：清欢
日期：2019/9/5  16:21
工具：python
python版本号3.7.0
"""
from utils.zhenzismsclient import ZhenziSmsClient as smsclient
import random
import json
phone={'telephone':'18569209745'}
def checking(tel):
    code = ''
    for num in range(1,5):
        code = code + str(random.randint(0,9))
    client = smsclient('https://sms_developer.zhenzikj.com',appId=102573,appSecret='NTVlMTg2MmEtMjY3OC00MWIyLTljMTMtMzdlNGFhYmI1ZjUw')
    res = client.send(tel,'您的乐游租车验证码为'+code+','+'验证码1分钟内有效。请不要泄露给他人，以免造成账号被盗的风险。')
    result = {"vf_code":code}
    result.update(json.loads(res))
    return result

# res=checking(phone['telephone'])
# print(res)