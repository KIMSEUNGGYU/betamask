from config import G, N
from signature import Signature
from random import randint

# deterministic 함수에서 필요 - 안전한 랜덤 수 만들기
import hashlib
import hmac

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret        # 개인키
        self.point = secret * G     # 공개키

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        """
        서명 생성 ?
        :param z: 메시지
        :return:
            Signature: 서명 객체 (r, s)
        """
        k = self.deterministic_k(z)
        r = (k * G).x.num
        k_inverse = pow(k, N-2, N)
        s = (z + r * self.secret) * k_inverse % N
        if s > N / 2:
            s = N - s
        return Signature(r=r, s=s)


    def deterministic_k(self, z):
        """
        비밀키(self) 와 메시지(z) 에 따라 랜덤 값 생성
        :param:
            self: 개인키
            z: 메시지
        :return:
            candidate: k 값으로 쓰기에 적당한 값
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
                return candidate # k 값으로 쓰기에 적당한 값
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()



    # k 의 중복을 고려하지 않은 코드
    # def sign(self, z):
    #     k = randint(0, N) #[0, N] 범위에서 무작위 값 생성
    #     r = (k * G).x.num # kG 의 x 좌표값
    #     k_inverse = pow(k, N-2, N) # 1/k
    #     s = (z + r * self.secret) * k_inverse % N # s = (z + re) / k
    #     # 비트코인 트랜잭션을 전파하는 노드는 가변성 문제로 N/2 보다 작은 x 값만을 전파함
    #     # 원래는 두개의 유효한 서명이 나옴 그래서 작은 x 값을 선택한다는 의미
    #     if s > N / 2:
    #         s = N - s
    #     return Signature(r=r, s=s) # 서명(r, s) 를 반환