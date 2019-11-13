"""
作者：清欢
日期：2019/8/12  14:00
工具：python
python版本号3.7.0
"""
from werkzeug.security import generate_password_hash,check_password_hash
from flask import jsonify

def encryption(str):
    temp=generate_password_hash(str,method='pbkdf2:sha1:2000',salt_length=8)
    return temp

def check_password(temp,str):
    res=check_password_hash(temp,str)
    return res