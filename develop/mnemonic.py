import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))

from src.privatekey import PrivateKey
from lib.mnemonic import Mnemonic
from lib.helper import (hash256, little_endian_to_int)

password_phrase = b"https://github.com/kimseunggyu gyu's password"      # 1. 비밀번호를 생성
secret = hash256(password_phrase)                                       # 2. 비밀번호를 알지 못하게 hash256 으로 해시
secret = little_endian_to_int(secret)                                   # 3. Private의 secret 은 정수이므로 바이트 값을 정수로 변환
private_key = PrivateKey(secret=secret)                                 # 4. Private 객체 생성 secret 과 공개키 생성


publick_key_hash160_value = private_key.point.hash160(compressed=True)  # 비압축 sec 방식 공개키 hash160 수행
print("공개키 hash160: ", publick_key_hash160_value.hex())

mnemonic = Mnemonic("english")                                          # 니모닉 객체 생성
print("mnemonic: ", mnemonic.to_mnemonic(publick_key_hash160_value))    # 니모닉 코드 생성