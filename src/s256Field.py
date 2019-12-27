# import os
# import sys
# sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))

from src.fieldElement import FieldElement
from lib.config import (PRIME)

class S256Field(FieldElement):
    """
    비트코인에서 유한체 클래스 정의
    """
    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=PRIME)

    def __repr__(self):
        # 원소를 화면에 보여줄때 256bit 자리를 채우기 위함. 빈자리가 생기면 b'0'으로 채움.
        # 256 bit -> 32byte -> 16진수로 64자리
        return '{:x}'.format(self.num).zfill(64) # 16진수로 넘어온 수를 표현, 단 64자리

    def sqrt(self):
        ## [(secp256k1) 에서] 직렬화할때 제곱근을 계산할때 w = v^(p+1)/4 임!
        return pow(self, (PRIME+1) // 4)