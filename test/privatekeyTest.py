import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase
from random import randint

from lib.helper import (run)
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






## 책 예제 테스트 코드 구현
run(S256Test("test_sign"))      # 개인키 서명 생성 및 검증 테스트