import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase
from random import randint

from lib.helper import (run, hash256, encode_base58)
from lib.config import (N)
from src.privatekey import PrivateKey

class S256Test(TestCase):
    def test_sign(self):
        print("********** [개인키 서명 생성 및 검증 테스트] **********")
        pk = PrivateKey(randint(0, N))              # 랜덤 키 생성
        z = randint(0, 2**256)                      # 랜덤 메시지 생성
        sig = pk.sign(z)                            # 메시지 서명 생성
        self.assertTrue(pk.point.verify(z, sig))    # verify 서명 검증
        # self.assertTrue(pk.public_key.verify(z, sig))

    def test_wif(self):
        print("********** [개인키 wif 테스트] **********")
        pk = PrivateKey(2**256 - 2**199)
        expected = 'L5oLkpV3aqBJ4BgssVAsax1iRa77G5CVYnv9adQ6Z87te7TyUdSC'
        self.assertEqual(pk.wif(compressed=True, testnet=False), expected)
        pk = PrivateKey(2**256 - 2**201)
        expected = '93XfLeifX7Jx7n7ELGMAf1SUR6f9kgQs8Xke8WStMwUtrDucMzn'
        self.assertEqual(pk.wif(compressed=False, testnet=True), expected)
        pk = PrivateKey(0x0dba685b4511dbd3d368e5c4358a1277de9486447af7b3604a69b8d9d8b7889d)
        expected = '5HvLFPDVgFZRK9cd4C5jcWki5Skz6fmKqi1GQJf5ZoMofid2Dty'
        self.assertEqual(pk.wif(compressed=False, testnet=False), expected)
        pk = PrivateKey(0x1cca23de92fd1862fb5b76e5f4f50eb082165e5191e116c18ed1a6b24be6a53f)
        expected = 'cNYfWuhDpbNM1JWc3c6JTrtrFVxU4AGhUKgw5f93NP2QaBqmxKkg'
        self.assertEqual(pk.wif(compressed=True, testnet=True), expected)

    def exercise1(self):
        print("********** [개인키 직렬화 wif 테스트] - raw 방식 **********")
        """
        비밀키 직렬화(wif) 생성 방식
        1. 메인넷 접두어 0x80, 테스트넷 접두어 0xef 로 시작
        2. 비밀키를 32바이트 길이의 빅엔디언으로 표현
        3. 대응하는 공개키를 압축 sec 로 표현했다면 2번 결과 뒤에 0x01 추가
        4. 1단계 결과 + 2단계 결과 + 3단계 결과
        5. 4번 결과에 hash256 하고 checksum 구하기 [:4]
        6. 4번 결과 + 5번 결과 후 Base58 로 부호화
        """
        testnet = True
        compressed = True

        private_key = PrivateKey(5003)
        secret_bytes = private_key.secret.to_bytes(32, 'big')  # 2 단계
        if testnet:                 # 1 단계
            prefix = b'\xef'
        else:
            prefix = b'\x80'

        if compressed:              # 3 단계
            suffix = b'\x01'
        else:
            suffix = b''

        result = prefix + secret_bytes + suffix     # 4 단계
        checksum = hash256(result)[:4]              # 5 단계
        wif = encode_base58(result + checksum)      # 6 단계
        print("result:", wif)

    def exercise2(self):
        # [연습 문제 4.6]
        print("********** [비밀키를 직렬화 wif]**********")
        # network(testnet), compressed, privateKey
        private_keys = ((True, True, 5003), (True, False, pow(2021, 5)), (False, True, 0x54321deadbeef))
        for is_testnet, is_compressed, private_key in private_keys:
            private = PrivateKey(private_key)
            print('wif 결과값 = ', private.wif(compressed=is_compressed, testnet=is_testnet))


## 책 예제 테스트 코드 구현
run(S256Test("test_sign"))      # 개인키 서명 생성 및 검증 테스트
run(S256Test("test_wif"))      # 개인키 서명 생성 및 검증 테스트


## 개인키 직렬화
# run(S256Test("exercise1"))      # 개인키 직렬화 wif 테스트 - raw 방식
# run(S256Test("exercise2"))      # 개인키 직렬화 wif 테스트


## 비트코인 주소 생성
