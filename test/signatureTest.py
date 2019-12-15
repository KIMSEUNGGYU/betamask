import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase
from random import randint

from lib.helper import run
from src.signature import Signature


class SignatureTest(TestCase):
    def test_der(self):
        print("********** [서명 직렬화 및 직렬화 값 복호화(원래값으로 되돌리기)] **********")
        testcases = (
            (1, 2),
            (randint(0, 2**256), randint(0, 2**255)),
            (randint(0, 2**256), randint(0, 2**255)),
        )
        for r, s in testcases:
            sig = Signature(r, s)
            print("기존의 서명 값: ", sig)
            der = sig.der()
            print("서명값 직렬화: ", der.hex())
            sig2 = Signature.parse(der)
            print("직렬화 된 값 복호화: ", sig2)
            print()
            self.assertEqual(sig2.r, r)
            self.assertEqual(sig2.s, s)

## 책 예제 테스트
# run(SignatureTest("test_der"))      # 서명 직렬화 및 직렬화 값 복호화(원래값으로 되돌리기)


