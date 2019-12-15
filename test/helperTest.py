import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase

from lib.helper import (run, little_endian_to_int, int_to_little_endian)

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


# run(HelperTest("test_little_endian_to_int"))        # bytes 값을 리틀엔디언으로 읽어서 정수로 변환
# run(HelperTest("test_int_to_little_endian"))        # 정수를 리틀엔디언 bytes 형 값으로 반환