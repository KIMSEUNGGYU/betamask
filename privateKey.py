from config import G, N
from signature import Signature
from random import randint

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = randint(0, N)
        r = (k * G).x.num
        k_inverse = pow(k, N-2, N)
        s = (z + r * self.secret) * k_inverse % N
        if s > N / 2: # 비트코인 트랜잭션을 전파하는 노드는 가변성 문제로 N/2 보다 작은 x 값만을 전파함
            s = N - s
        return Signature(r=r, s=s)