from cryptography.fernet import Fernet


# 解密
def decrypt_token(encrypted_token, key):
    f = Fernet(key)
    decrypted_token = f.decrypt(encrypted_token.encode()).decode()
    return decrypted_token
