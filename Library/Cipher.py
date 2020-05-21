import base64
import hashlib
import platform
import Crypto
import rsa
import uuid

def UUID():
    return ''.join(str(uuid.uuid4()).split('-'))

def MD5Encrypt(Data):
    return hashlib.md5(Data.encode()).hexdigest()

def SHA256Encrypt(Data):
    return hashlib.sha256(Data.encode()).hexdigest()



def Base64Encrypt(Data):
    return base64.b64encode(Data)

def Base64Decrypt(Data):
    return base64.b64decode(Data)

def DEAEncrypt(Data):
    pass

def DEADecrypt(Data):
    pass

def TDESEncrypt(Data):
    pass

def TDESDecrypt(Data):
    pass

def AESEncrypt(Data):
    pass

def AESDecrypt(Data):
    pass

def DEAEncrypt(Data):
    pass

def DEADecrypt(Data):
    pass



def RSACertificationGenerate():
    pass

def RSAEncrypt(Data):
    pass

def RSADecrypt(Data):
    pass