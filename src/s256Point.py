import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))

from src.point import Point
from src.s256Field import S256Field
from lib.config import (A, B, N, GX, GY)

class S256Point(Point):
    """
    공개키 클래스
    secp256k1 타원곡선 상에 점!
    """

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)
            # 무한원점으로 초기화하는 경우(x=None)를 고려해서 x와 y 값을 S256Field 클래스의 인스턴스로 주지않고 인수로 받은 값을 그대로 넘겨줌

    def __repr__(self):
        if self.x is None:
            return 'S256Point(무한원점[항등원])'
        else:
            return f'S256Point({self.x}, {self.y})'

    def __rmul__(self, coefficient):
        coef = coefficient % N # 우한순환군 rmul 연산?, nG = 0 이므로, n 번마다 다시 0 (무한원점) 으로 되돌아옴
        return super().__rmul__(coef)

    def verify(self, z, signature):
        """
        공개키로 서명을 검증하니깐 공개키 클래스에 서명 검증하는 기능 구현
        :param z: 메시지 z
        :param signature: signature 안에는 (r, s) 가 들어있음
        :return:
        """
        G = S256Point(GX, GY)                   # 생성점 G
        s_inverse = pow(signature.s, N-2, N)    # signatrue 의 s 의 역원인 "1/s" - 페르마의 소정리
        u = z * s_inverse                       # u = z / s
        v = signature.r * s_inverse             # v = r / s
        total = u * G + v * self                # self 는 public_key 따라서, uG + vP
        return total.x.num == signature.r
