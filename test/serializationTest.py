import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase

from lib.helper import (run, encode_base58, hash160, hash256)
from src.privatekey import PrivateKey
from src.signature import Signature


class SerializationTest(TestCase):
    def exercise1(self):
        # [연습문제 4.1]
        print("********** [비밀키에 대응하는 공개키를 비압축 SEC 형식으로 구하기] **********")

        private_values = (5000, pow(2018, 5), 0xdeadbeef12345)
        for private_value in private_values:
            private_key = PrivateKey(secret=private_value)
            print(f'비밀키 {private_value} 공개키 비압축 방식으로 직렬화한 값 = ', private_key.point.sec(compressed=False).hex()) # 마지막에 hex() 넣은 이유는 보기 편하고자

    def exercise2(self):
        # [연습문제 4.2]
        print("********** [비밀키에 대응하는 공개키를 압축 SEC 형식으로 구하기] **********")

        private_values = (5001, pow(2019, 5), 0xdeadbeef54321)
        for private_value in private_values:
            private_key = PrivateKey(secret=private_value)
            print(f'비밀키 {private_value} 공개키 압축방식으로 직렬화한 값 = ', private_key.point.sec(compressed=True).hex()) # 마지막에 hex() 넣은 이유는 보기 편하고자

    def exercise3(self):
        print("********** [비밀키에 대응하는 공개키를 압축 SEC 형식으로 직렬화된 값을 역질렬화(parse) 하기] **********")
        private_key = PrivateKey(secret=5001)
        sec_binary =  private_key.point.sec(compressed=True)
        print("기존 공개키: ", private_key.point)
        print("역직렬화: ", private_key.point.parse(sec_binary))

    def exercise4(self):
        print("********** [서명 값 확인 및 der 결과 값 확인] **********")
        r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        signature = Signature(r, s)
        serialization_signature = signature.der()
        print('서명값 직렬화하기', serialization_signature.hex())
        # print(signature)

    def exercise5(self):
        print("********** [r 과 s 값의 서명을 DER 형식으로 직렬화하기] **********")
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec

        signature = Signature(r=r, s=s)
        serialization_signature = signature.der()
        print('서명값 직렬화하기: ', serialization_signature.hex())


    def exercise6(self):
        print("********** [16진수 값을 bytes 형 값으로 변경 후 이를 다시 base58 로 인코딩 하기] **********")
        hex_values = ('7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d', 'eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c', 'c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6')

        for hex in hex_values:
            print("BASE58 ENCODE VALUE:", encode_base58(bytes.fromhex(hex))) # 해시 값을 byte 로 변환후 base58로 인코딩

    def exercise7(self):
        print("********** [비트코인 주소 생성하기 raw 방식으로 - 테스트넷] **********")
        '''
        비트코인 주소 생성 방식
        1. 메인넷은 0x00 으로 시작, 테스트넷은 0x6f 로 시작
        2. sec 형식 주소를 hash160 방식을 사용해서 출력값을 얻음
        3. 1단계의 값과 2단계의 값을 합침
        4. 3에서 얻은 결과를 hash256 하고, 그 결과의 첫 4바이트 취함 <- checksum 구하기
        5. 3의 결과 뒤에 4의 결과를 붙이고 BASE58로 부호화
        '''
        private_key = PrivateKey(5002)

        prefix = b'\x6f' # 1단계
        sec = hash160(private_key.point.sec(compressed=False)) # 비압축 sec 생성, 2단계
        result = prefix + sec                       # 3 단계

        print('result: ', result.hex())

        check_sum = hash256(result)[:4]             # 4단계
        result = encode_base58(result + check_sum)  # 5단계
        print("비트코인 주소 =", result)

    def exercise8(self):
        # [연습문제 4.5]
        print("********** [비밀키에 대응하는 공개키를 구하고 비트코인 주소 구하기] - 기능 정의한 것들로 **********")
        # network(testnet), compressed, privateKey
        private_keys = ((True, False, 5002), (True, True, pow(2020, 5)), (False, True, 0x12345deadbeef))
        for is_testnet, is_compressed, private_key in private_keys:
            public_key = PrivateKey(private_key).point      # 공개키 받고
            bitcoin_address = public_key.address(compressed=is_compressed, testnet=is_testnet)
            print("bitcoin address = ", bitcoin_address)
















## 책 예제 테스트 코드 구현

## 공개키 직렬화 테스트
# run(SerializationTest("exercise1"))         # 비밀키에 대응하는 공개키를 비압축 SEC 형식으로 구하기
# run(SerializationTest("exercise2"))         # 비밀키에 대응하는 공개키를 압축 SEC 형식으로 구하기
# run(SerializationTest("exercise3"))         # 비밀키에 대응하는 공개키를 압축 SEC 형식으로 직렬화된 값을 역질렬화(parse) 하기

## 서명 직렬화 테스트
# run(SerializationTest("exercise4"))         # 서명 값 확인 및 der 결과 값 확인
# run(SerializationTest("exercise5"))         # r 과 s 값의 서명을 DER 형식으로 직렬화하기

## 비트코인 주소 테스트
# run(SerializationTest("exercise6"))         # 16진수 값을 bytes 형 값으로 변경 후 이를 다시 base58 로 인코딩 하기
# run(SerializationTest("exercise7"))         # 비트코인 주소 생성하기 raw 방식으로 - 테스트넷
# run(SerializationTest("exercise8"))         # 비밀키에 대응하는 공개키를 구하고 비트코인 주소 구하기

## 비밀키 WIF 테스트 <- privateKeyTest 에 있음

