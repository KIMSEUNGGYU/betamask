# import os
# import sys
# sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))

from src.point import Point
from src.s256Field import S256Field
from lib.config import (A, B, N, GX, GY, PRIME)
from lib.helper import (hash160, encode_base58_checksum)

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

    def sec(self, compressed=True):
        """
        ECDSA 공개키 직렬화 표준인 SEC 방식 적용
        직렬화 하는 기능 - 바이트 값이 나옴
        1. 비압축 방식
        2. 압축 방식
        :return:
            bytes: 직렬화 한 값
        """

        if compressed:
            # 압축 방식
            if self.y.num % 2 == 0: # 짝수인 경우
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:   # 홀수인 경우
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            # int.to_bytes :  정수형 숫자를 bytes 형으로 반환
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big') # 비압축 방식


    @classmethod
    def parse(self, sec_binary):
        """
        직렬화 된 값(bytes 형태)을 기존형태인 공개키 형식으로 만듦 (x, y)
        :return:
            S256Point: 공개키 객체
        """
        """returns a Point Object from a SEC binary (not hex)"""

        # 비압축 방식
        if sec_binary[0] == 4:                                  # 비압축 방식
            x = int.from_bytes(sec_binary[1:33], 'big')         # 1byte 는 구분자, 이후 x 좌표값 32byte
            y = int.from_bytes(sec_binary[33:65], 'big')        # x좌표 이후 32byte 는 y
            return S256Point(x=x, y=y)

        # 압축 방식 - 구분자 제외하면 x좌표만 있음
        is_even = sec_binary[0] == 2                            # 압축 방식 - 첫 byte 가 2이면 짝수
        x = S256Field(int.from_bytes(sec_binary[1:], 'big'))    # x 값, 직렬한 값을 정수로 변경


        ## x 좌표를 이용해 y 좌표를 구하기, 타원곡선 y^2 = x^3 + 7
        ## 하지만, 이때 우리는 w^2 = v 로 두고 식을 유도해 제곱근을 구했음. (S256Field 의 sqrt 로 구현함)
        ## w = v^(p+1)/4 # 이때 v 는 타원곡선 식 (x^3 + 7) 이고, w = y^2 을 의미
        v = pow(x, 3) + S256Field(B)                            # x^3 + 7
        w = v.sqrt()                                            # y 값, v 를 이용해 w (y) 값 구하기 -> 이는 "v^(p+1)/4"

        if w.num % 2 == 0:      # 위에서 구한 y(w) 값이 짝수인 경우
            even_w = w
            odd_w = S256Field(PRIME - w.num)
        else:                   # 위에서 구한 y(w) 값이 홀수인 경우
            even_w = S256Field(PRIME - w.num)
            odd_w = w

        ## 각각의 값(x 와 y)들을 구하고 공개키 객체로 만듦
        if is_even:
            return S256Point(x, even_w)
        else:
            return S256Point(x, odd_w)

    def hash160(self, compressed=True):
        """
        공개키에서 hash160 을 하는 이유는 비트코인 주소를 생성할 때 사용
        이때, 공개키를 sec 방식으로 직렬화하고 해당 값을 hash160 수행
        :param compressed:
        :return:
        """
        return hash160(self.sec(compressed=compressed))

    def address(self, compressed=True, testnet=False):
        """
        비트코인 주소를 생성하는 기능

        비트코인 주소 생성 방식
        1. 메인넷은 0x00 으로 시작, 테스트넷은 0x6f 로 시작
        2. sec 형식 주소를 hash160 방식을 사용해서 출력값을 얻음
        3. 1단계의 값과 2단계의 값을 합침
        4. 3에서 얻은 결과를 hash256 하고, 그 결과의 첫 4바이트 취함 <- checksum 구하기
        5. 3의 결과 뒤에 4의 결과를 붙이고 BASE58로 부호화

        :param compressed: sec 을 수행할 때 어떤 방식으로 할지
        :param testnet: 테스트넷인지 메인넷인지
        :return:
        """
        hash160_value = self.hash160(compressed=compressed)     # sec 값을 hash160 으로 해시, 2 단계
        if testnet:                                             # 메인넷인지, 테스트넷인지 접두어 구함 , 1단계
            prefix = b'\x6f'
        else:
            prefix = b'\x00'

        return encode_base58_checksum(prefix + hash160_value)   # 3단계를 보내고 encode_base58_checksum() 에서 4, 5 단계 수행
