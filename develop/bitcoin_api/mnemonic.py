import os
import sys
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]     # 상위 디렉토리 추출
path = os.path.split(path)[0]                                           # 상위 디렉토리 추출
sys.path.append(path)                                                   # path 지정

from src.privatekey import PrivateKey
from lib.mnemonic import Mnemonic
from lib.helper import (hash256, little_endian_to_int, decode_base58)

def get_bitcoin_address(password):
    """
    비트코인 주소 가져오기 (생성 후 가져 옴)
    :param password: 사용자의 비밀번호
    :return:
    """

    password = password.encode()                            # 1. 비밀번호를 생성
    secret = hash256(password)                              # 2. 비밀번호를 알지 못하게 hash256 으로 해시
    secret = little_endian_to_int(secret)                   # 3. Private의 secret 은 정수이므로 바이트 값을 정수로 변환
    private_key = PrivateKey(secret=secret)                 # 4. Private 객체 생성 secret 과 공개키 생성

    bitcoin_address = private_key.point.address(compressed=True, testnet=True)  # 비밀번호를 이용하여 비트코인 주소 생성
    return bitcoin_address


def make_mnemonic(address):
    """
    비트코인 주소를 이용해 니모닉 코드 생성
    :param address:
    :return:
    """
    hash160_value = decode_base58(address)
    mnemonic = Mnemonic("english")
    return mnemonic.to_mnemonic(hash160_value)