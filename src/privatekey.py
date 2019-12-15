from lib.config import (GX, GY, N)
from src.s256Point import S256Point
from src.signature import Signature
from lib.helper import (encode_base58_checksum)

## 안전한 키값을 생성하기 위해 필요
import hashlib
import hmac


class PrivateKey:
    """
    개인키 클래스
    메시지 서명을 생성하기 위해 비밀키를 보관?
    """
    def __init__(self, secret):
        """
        :param secret: 개인키 값 e
        """
        G = S256Point(GX, GY)
        self.secret = secret                # 개인키 e
        self.point = secret * G             # 공개키
        # self.public_key = secret * G        # 공개키 <- 원래는 public_key 로 정의하고자 했으나, 이후에 에러가 발생할거 같아 후에 바꿀예정

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)     # 개인키 값을 16진수 64 글자로 보여줌

    def sign(self, z):
        """
        메시지 서명 생성
        :param z: 메시지
        :return:
        """
        G = S256Point(GX, GY)                   # 생성점 G
        k = self.deterministic_k(z)             # k 값을 무작위로 설정하지 않고 개인키(self.secret) 와 서명해시(z) 에 따라 결정
        k_inverse = pow(k, N-2, N)              # 랜덤 값 k 의 역수인 "1/k"

        r = (k*G).x.num                         # r = (k * G) = (x, y) 의 x 좌표값
        s = (z + r*self.secret) * k_inverse % N # s = (z + r*e) / k <- 이 k 때문에 k_inverse 필요

        # 비트코인 트랜잭션을전파하는 노드는 가변성 문제로 N/2 보다 작은 s 값만을 전파함.
        # 즉, 같은 공개키 암호화 방식을 이용해서 같은 서명 값이 나올 수 있음.
        # 서명 (r, s) 와 서명 (r, N-s) 값이 나올 수 있어 2개의 유효한 TxID 가 존재해, low s 값만 사용
        if s > N/2:
            s = N - s
        return Signature(r=r, s=s)

    def deterministic_k(self, z):
        """
        개인키(self.secret) 와 메시지(z) 를 통해 k를 유일하게 생성하는 방법 RFC6979
        :param z: 메시지
        :return: k 값으로 알맞은 값
        """

        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if candidate >= 1 and candidate < N:
                return candidate  # k 값으로 알맞은 값
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()

    def wif(self, compressed=True, testnet=False):
        """
        비밀키 직렬화 - 비밀키를 읽기 쉽도록 (잘 사용하지 않고, 주로 지갑을 다른 지갑을 옮기고 싶을때 사용)

        비밀키 직렬화(wif) 생성 방식
        1. 메인넷 접두어 0x80, 테스트넷 접두어 0xef 로 시작
        2. 비밀키를 32바이트 길이의 빅엔디언으로 표현
        3. 대응하는 공개키를 압축 sec 로 표현했다면 2번 결과 뒤에 0x01 추가
        4. 1단계 결과 + 2단계 결과 + 3단계 결과
        5. 4번 결과에 hash256 하고 checksum 구하기 [:4]
        6. 4번 결과 + 5번 결과 후 Base58 로 부호화

        :param compressed:  sec 압축 방식이었는지
        :param testnet:     테스트넷 wif 를 생성할지
        :return:
        """

        secret_bytes = self.secret.to_bytes(32, 'big')  # 2 단계
        if testnet:                                     # 1 단계
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:                                  # 3 단계
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)   # 4 단계 수행 후 encode_base58_checksum 기능 수행(5, 6 단계)