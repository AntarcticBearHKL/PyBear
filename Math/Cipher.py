import base64
import hashlib
import platform
import Crypto
import rsa
import uuid
from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex

def UUID():
    return ''.join(str(uuid.uuid4()).split('-'))

def NumberIndex():
    return str(abs(hash(UUID())))

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

def AESEncrypt(Data, Key):
    AESCryptor = AES.new(MD5Encrypt(Key)[:16].encode('utf-8'), AES.MODE_CBC, MD5Encrypt(Key)[16:].encode('utf-8'))
    Data = Data.encode('utf-8')
    BNTP = AES.block_size - (len(Data) % AES.block_size)
    Data += BNTP * bytes([BNTP])
    CipherData = AESCryptor.encrypt(Data)
    return base64.b64encode(b2a_hex(CipherData)).decode('utf8')

def AESDecrypt(Data, Key):
    Unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    CipherData = base64.b64decode(Data.encode('utf8'))
    AESCryptor = AES.new(MD5Encrypt(Key)[:16].encode('utf-8'), AES.MODE_CBC, MD5Encrypt(Key)[16:].encode('utf-8'))
    Ret = AESCryptor.decrypt(a2b_hex(CipherData))
    Ret = str(Unpad(Ret), encoding='utf8')
    return Ret

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