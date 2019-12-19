import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase

from lib.helper import run
from src.script import Script



class ScriptTest(TestCase):
    def exercise1(self):
        print("********** [스크립트 p2pk 테스트 ] **********")
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        sec_public_key = bytes.fromhex('04887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34')
        signature = bytes.fromhex('3045022000eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c022100c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab601') # der 형식?
        script_public_key = Script([sec_public_key, 0xac])     # 잠금 스크립트 - [공개키_값, OP_CHECKSIGNATURE] 0xac = 172
        script_signature = Script([signature])      # 해제 스크립트 - [서명_값]
        combined_script = script_signature + script_public_key
        print("p2pk 스크립트 실행: ", combined_script.evaluate(z))

    def exercise2(self):
        print("********** [잠금스크립트를 해제하는 해제스크립트 작성하기 테스트 ] **********")
        # script_pubkey = Script([0x76, 0x76, 0x95, 0x93, 0x56, 0x87])
        # script_sig = Script([])  # FILL THIS IN
        # combined_script = script_sig + script_pubkey
        # print(combined_script.evaluate(0))
        ####### 안됨.. 왜냐하면 OP_MUL 이 구현되어 있지 않음..
        # script_public_key = Script([0x76, 0x76, 0x95, 0x93, 0x56, 0x87])
        # script_signature = Script([0x52])
        # combined_script = script_signature + script_public_key
        # print(combined_script.evaluate(0))

    def exercise3(self):
        print("********** [잠금스크립트를 해제하는 해제스크립트 작성하기 테스트 ] **********")
        ## c1, c2 값이 없음
        # script_pubkey = Script([0x6e, 0x87, 0x91, 0x69, 0xa7, 0x7c, 0xa7, 0x87])
        # script_sig = Script([])  # FILL THIS IN
        # combined_script = script_sig + script_pubkey
        # print(combined_script.evaluate(0))



run(ScriptTest("exercise1"))
run(ScriptTest("exercise2"))
run(ScriptTest("exercise3"))