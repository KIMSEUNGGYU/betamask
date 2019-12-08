from point import Point
from s256Field import S256Field

## 비트코인에서 사용하는 secp256k1 에서 정의한 값
## 하지만 여기서는 A, B 값만 사용
A = 0
B = 7
# P = pow(2, 256) - pow(2, 32) - 977
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

# end::source10[]
class S256Point(Point):
    """
    secp256k1 에서의 점 객체 정의
    비트코인에서 사용하는 점 객체 정의
    1. y^2 = x^3 + bx + 7 에서 a = 0, b = 7
    2. 유한체 위수 소수 p = pow(2, 256) - pow(2, 32) - 977
    3. 생성점 G의 x와 y 좌표값
        x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
        y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    4. 군의 위수 n
        n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
    """
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)

        ## x 값이 점이 아닌 값이면 점으로 만들고 객체 생성
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __rmul__(self, coefficient):
        coef = coefficient % N # nG 는 0 이므로 n 으로 나눈 나머지를 구하는 나머지 연산을 할 수 있음.
        # 즉 n 번마다 다시 0(무한원점) 으로 되돌아옴
        return super().__rmul__(coef)

    def verify(self, z, sign):
        G = S256Point(
            0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
            0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8)

        sign_inv = pow(sign.s, N-2, N) # 1/s 구하기
        u = z * sign_inv % N
        v = sign.r * sign_inv % N
        R = u * G + v * self # self 가 public 키 값
        return R.x.num == sign.r

