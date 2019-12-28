import os
import sys
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
sys.path.append(os.path.abspath(path))

from unittest import TestCase

from lib.helper import (run, little_endian_to_int, int_to_little_endian, decode_base58, encode_base58_checksum)

class HelperTest(TestCase):
    def test_little_endian_to_int(self):
        # [연습 문제 4.7]
        print("********** [bytes 값을 리틀엔디언으로 읽어서 정수로 변환] **********")
        h = bytes.fromhex('99c3980000000000')
        want = 10011545
        self.assertEqual(little_endian_to_int(h), want)
        h = bytes.fromhex('a135ef0100000000')
        want = 32454049
        self.assertEqual(little_endian_to_int(h), want)

    def test_int_to_little_endian(self):
        # [연습 문제 4.8]
        print("********** [정수를 리틀엔디언 bytes 형 값으로 반환] **********")
        n = 1
        want = b'\x01\x00\x00\x00'
        self.assertEqual(int_to_little_endian(n, 4), want)
        n = 10011545
        want = b'\x99\xc3\x98\x00\x00\x00\x00\x00'
        self.assertEqual(int_to_little_endian(n, 8), want)

    def test_base58(self):
        print("********** [base58 인코딩, 디코딩 테스트] **********")

        addr = 'mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf'
        h160 = decode_base58(addr).hex()
        want = '507b27411ccf7f16f10297de6cef3f291623eddf'
        self.assertEqual(h160, want)
        got = encode_base58_checksum(b'\x6f' + bytes.fromhex(h160))
        self.assertEqual(got, addr)

# run(HelperTest("test_little_endian_to_int"))        # bytes 값을 리틀엔디언으로 읽어서 정수로 변환
# run(HelperTest("test_int_to_little_endian"))        # 정수를 리틀엔디언 bytes 형 값으로 반환
# run(HelperTest("test_base58"))                      # base58 인코딩, 디코딩 테스트