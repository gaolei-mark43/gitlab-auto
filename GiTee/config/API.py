import requests
import GiTee.config.config as config
import GiTee.config.decrypt_token as decrypt_token


# 读取配置文件
def get_config():
    baseurl = config.baseUrl
    key = config.key
    encrypted_token = config.encrypted_token
    PRIVATE_TOKEN = decrypt_token.decrypt_token(encrypted_token, key)
    return baseurl, PRIVATE_TOKEN


