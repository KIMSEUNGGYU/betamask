import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))


from src.privatekey import PrivateKey
from lib.helper import (hash256, little_endian_to_int)

def createBitcoinAddress():
    # [연습 문제 4.9]
    print("비트코인 주소를 생성합니다.")
    """
    자신만의 비밀키로 테스트넷 주소에서 사용 가능한 비트코인 주소를 만들기
    비트코인 주소를 이용해서 테스트 넷 코인 발행까지 해보기
    """

    password_phrase = b"https://github.com/kimseunggyu gyu's password"  # 1. 비밀번호를 생성
    secret = hash256(password_phrase)                                   # 2. 비밀번호를 알지 못하게 hash256 으로 해시
    # print("secret:", secret.hex())
    secret = little_endian_to_int(secret)                               # 3. Private의 secret 은 정수이므로 바이트 값을 정수로 변환
    private_key = PrivateKey(secret=secret)                             # 4. Private 객체 생성 secret 과 공개키 생성
    # print("private_key = ", private_key.secret)
    bitcoin_address = private_key.point.address(testnet=True, compressed=True) # testnet, 압축 방식으로 비트코인 주소 생성
    print("bitcoin_address = ", bitcoin_address)    # mtSYsqiRFrfaTAN7y1EvBb3CBEadEF1a9R



createBitcoinAddress()