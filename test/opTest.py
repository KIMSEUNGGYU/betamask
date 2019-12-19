import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase

from lib.helper import run

from src.op import (op_hash160, op_checksignature, decode_num)


class OPTest(TestCase):
    def test_op_hash160(self):
        print("********** [OP_HASH160 연산 테스트] **********")
        stack = [b'hello world']
        self.assertTrue(op_hash160(stack))
        self.assertEqual(stack[0].hex(),'d7d5ee7824ff93f94c3055af9382c86c68b5ca92')

    def test_op_checksig(self):
        print("********** [OP_CHECKSIG 연산 테스트] **********")
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        sec = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
        sig = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601')

        stack = [sig, sec]      # op연산을 하기위한 스택 데이터, 서명과 공개키 값
        self.assertTrue(op_checksignature(stack, z))    # 1. 서명 검증 연산
        self.assertEqual(decode_num(stack[0]), 1)       # 2. 서명 검증이 참인지 확인


run(OPTest("test_op_hash160"))          # OP_HASH160 연산 테스트
run(OPTest("test_op_checksig"))         # OP_CHECKSIG 연산 테스트
