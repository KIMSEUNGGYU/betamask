import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
from unittest import TestCase

from src.point import Point
from src.fieldElement import FieldElement
from src.s256Point import S256Point
from src.signature import Signature
from lib.helper import (run, hash256)
from lib.config import (GX, GY, A, B, PRIME, N)


class S256Test(TestCase):
    def test_order(self):
        print("********** [유한순환군의 N 인지 확인하는 기능 구현] **********")
        G = S256Point(GX, GY)
        point = N * G
        self.assertIsNone(point.x)

    def test_pubpoint(self):
        print("********** [비밀키와 공개키 일치하는지 확인] **********")
        G = S256Point(GX, GY)
        # write a test that tests the public point for the following
        points = (
            # secret, x, y
            (7, 0x5cbdf0646e5db4eaa398f365f2ea7a0e3d419b7e0330e39ce92bddedcac4f9bc, 0x6aebca40ba255960a3178d6d861a54dba813d0b813fde7b5a5082628087264da),
            (1485, 0xc982196a7466fbbbb0e27a940b6af926c1a74d5ad07128c82824a11b5398afda, 0x7a91f9eae64438afb9ce6448a1c133db2d8fb9254e4546b6f001637d50901f55),
            (2**128, 0x8f68b9d2f63b5f339239c1ad981f162ee88c5678723ea3351b7b444c9ec4c0da, 0x662a9f2dba063986de1d90c2b6be215dbbea2cfe95510bfdf23cbf79501fff82),
            (2**240 + 2**31, 0x9577ff57c8234558f293df502ca4f09cbc65a6572c842b39b366f21717945116, 0x10b49c67fa9365ad7b90dab070be339a1daf9052373ec30ffae4f72d5e66d053),
        )

        # iterate over points
        for secret, x, y in points:
            # initialize the secp256k1 point (S256Point)
            point = S256Point(x, y)
            # check that the secret*G is the same as the point
            self.assertEqual(secret * G, point)

    def test_verify(self):
        print("********** [전자 서명 검증 기능 테스트] **********")
        point = S256Point(
            0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c,
            0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34)
        z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
        r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        self.assertTrue(point.verify(z, Signature(r, s)))
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
        s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
        self.assertTrue(point.verify(z, Signature(r, s)))

    def test_sec(self):
        print("********** [공개키 SEC 직렬화 테스트] **********")
        G = S256Point(GX, GY)
        coefficient = 999**3
        uncompressed = '049d5ca49670cbe4c3bfa84c96a8c87df086c6ea6a24ba6b809c9de234496808d56fa15cc7f3d38cda98dee2419f415b7513dde1301f8643cd9245aea7f3f911f9'
        compressed = '039d5ca49670cbe4c3bfa84c96a8c87df086c6ea6a24ba6b809c9de234496808d5'
        point = coefficient * G
        self.assertEqual(point.sec(compressed=False), bytes.fromhex(uncompressed))
        self.assertEqual(point.sec(compressed=True), bytes.fromhex(compressed))
        coefficient = 123
        uncompressed = '04a598a8030da6d86c6bc7f2f5144ea549d28211ea58faa70ebf4c1e665c1fe9b5204b5d6f84822c307e4b4a7140737aec23fc63b65b35f86a10026dbd2d864e6b'
        compressed = '03a598a8030da6d86c6bc7f2f5144ea549d28211ea58faa70ebf4c1e665c1fe9b5'
        point = coefficient * G
        self.assertEqual(point.sec(compressed=False), bytes.fromhex(uncompressed))
        self.assertEqual(point.sec(compressed=True), bytes.fromhex(compressed))
        coefficient = 42424242
        uncompressed = '04aee2e7d843f7430097859e2bc603abcc3274ff8169c1a469fee0f20614066f8e21ec53f40efac47ac1c5211b2123527e0e9b57ede790c4da1e72c91fb7da54a3'
        compressed = '03aee2e7d843f7430097859e2bc603abcc3274ff8169c1a469fee0f20614066f8e'
        point = coefficient * G
        self.assertEqual(point.sec(compressed=False), bytes.fromhex(uncompressed))
        self.assertEqual(point.sec(compressed=True), bytes.fromhex(compressed))

    def test_address(self):
        print("********** [비트코인 주소 테스트] **********")
        G = S256Point(GX, GY)
        secret = 888**3
        mainnet_address = '148dY81A9BmdpMhvYEVznrM45kWN32vSCN'
        testnet_address = 'mieaqB68xDCtbUBYFoUNcmZNwk74xcBfTP'
        point = secret * G
        self.assertEqual(
            point.address(compressed=True, testnet=False), mainnet_address)
        self.assertEqual(
            point.address(compressed=True, testnet=True), testnet_address)
        secret = 321
        mainnet_address = '1S6g2xBJSED7Qr9CYZib5f4PYVhHZiVfj'
        testnet_address = 'mfx3y63A7TfTtXKkv7Y6QzsPFY6QCBCXiP'
        point = secret * G
        self.assertEqual(
            point.address(compressed=False, testnet=False), mainnet_address)
        self.assertEqual(
            point.address(compressed=False, testnet=True), testnet_address)
        secret = 4242424242
        mainnet_address = '1226JSptcStqn4Yq9aAmNXdwdc2ixuH9nb'
        testnet_address = 'mgY3bVusRUL6ZB2Ss999CSrGVbdRwVpM8s'
        point = secret * G
        self.assertEqual(
            point.address(compressed=False, testnet=False), mainnet_address)
        self.assertEqual(
            point.address(compressed=False, testnet=True), testnet_address)


    def exercise1(self):
        print("********** [SECP256k1 곡선의 생성점 G 가 y^2 = x^3 + 7 위에 있는지 확인] **********")
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798 # 생성점 x 좌표
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8 # 생성점 y 좌표
        prime = pow(2, 256) - pow(2, 32) - 977 # 위수
        print("생성점 G가 타원곡선 y^2 = x^3 + 7 위에 있나요?", pow(gy, 2) % prime == (pow(gx, 3) + 7) % prime)

    def exercise2(self):
        print("********** [SECP256k1 곡선의 생성점 G로 생성한 군의 위수가 n 인지 확인] **********")
        gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798 # 생성점 x 좌표
        gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8 # 생성점 y 좌표
        prime = pow(2, 256) - pow(2, 32) - 977 # 위수
        n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

        x = FieldElement(gx, prime)
        y = FieldElement(gy, prime)
        a =  FieldElement(0, prime)
        b =  FieldElement(7, prime)
        G = Point(x, y, a, b)
        print("생성점 G의 위수가 n 인가요?", n * G)

    def exercise3(self):
        print("********** [SECP256k1 곡선의 생성점 G로 생성한 군의 위수가 n 인지 확인] - config 변수 사용 **********")
        x = FieldElement(GX, PRIME)
        y = FieldElement(GY, PRIME)
        a =  FieldElement(A, PRIME)
        b =  FieldElement(B, PRIME)
        G = Point(x, y, a, b)
        print("생성점 G의 위수가 n 인가요?", N * G)

    def exercise4(self):
        print("********** [G 로 생성한 군의 위수가 n 이라는 것을 확인 하기] **********")
        G = S256Point(GX, GY)
        print("N * G = ",  N * G)

    def exercise5(self):
        print("********** [서명 검증] **********")
        z = 0xbc62d4b80d9e36da29c16c5d4d9f11731f36052c72401a76c23c0fb5a9b74423
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        public_key_x = 0x04519fac3d910ca7e7138f7013706f619fa8f033e6ec6e09370ea38cee6a7574
        public_key_y = 0x82b51eab8c27c66e26c858a079bcdf4f1ada34cec420cafc7eac1a42216fb6c4

        public_point = S256Point(public_key_x, public_key_y)
        G = S256Point(GX, GY)
        s_inverse = pow(s, N-2, N)      # 페르마의 소정리로 "1/s" 를 의미
        u = z * s_inverse % N           # z / s
        v = r * s_inverse % N           # r / s
        print("서명이 유효한가요? ", (u*G + v*public_point).x.num == r) # uG + vP = R 의 x 좌표가 r 이랑 동일한지 비교

    def exercise6(self):
        # [연습문제 3.6]
        print("********** [2개의 서명이 유효한지 확인] **********")
        public_key_x = 0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c
        public_key_y = 0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34
        public_key = S256Point(public_key_x, public_key_y)

        # 서명 1
        z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
        r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4
        # uG + vP
        G = S256Point(GX, GY)
        s_inverse = pow(s, N-2, N)
        u = z * s_inverse
        v = r * s_inverse
        print("서명 1 이 유효한가요? ", (u * G + v * public_key).x.num == r)

        # 서명 2
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
        s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6
        # uG + vP
        G = S256Point(GX, GY)
        s_inverse = pow(s, N-2, N)
        u = z * s_inverse
        v = r * s_inverse
        print("서명 2가 유효한가요? ", (u * G + v * public_key).x.num == r)

    def exercise7(self):
        # [연습문제 3.6]
        print("********** [2개의 서명이 유효한지 확인] - s256Point verify 기능 사용 **********")
        public_key_x = 0x887387e452b8eacc4acfde10d9aaf7f6d9a0f975aabb10d006e4da568744d06c
        public_key_y = 0x61de6d95231cd89026e286df3b6ae4a894a3378e393e93a0f45b666329a0ae34
        public_key = S256Point(public_key_x, public_key_y)

        # 서명 1
        z = 0xec208baa0fc1c19f708a9ca96fdeff3ac3f230bb4a7ba4aede4942ad003c0f60
        r = 0xac8d1c87e51d0d441be8b3dd5b05c8795b48875dffe00b7ffcfac23010d3a395
        s = 0x68342ceff8935ededd102dd876ffd6ba72d6a427a3edb13d26eb0781cb423c4

        signature = Signature(r, s)
        print("서명 1이 유효한가요? ", public_key.verify(z=z, signature=signature))

        # 서명 2
        z = 0x7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d
        r = 0xeff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c
        s = 0xc7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6

        signature = Signature(r, s)
        print("서명 2가 유효한가요? ", public_key.verify(z, signature))

    def exercise8(self):
        print("********** [서명 생성] **********")
        # int.from_bytes                                        # byte 값들을 정수로 변환
        e = int.from_bytes(hash256(b'my secret'), 'big')        # 비밀키, 즉 개인키 생성
        z = int.from_bytes(hash256(b'my message'), 'big')       # 서명해시, 메시지 해시 생성
        k = 1234567890                                          # 원래는 랜덤값
        G = S256Point(GX, GY)                                   # 생성점 G
        k_inverse = pow(k, N-2, N)                              # 랜덤값 k 의 역원 "1/k"

        r = (k*G).x.num                                         # k*G = (x, y)를 계산후 x 의 좌표만 사용
        s = (z + r*e) * k_inverse % N                           # s = (z + re) / k
        public_key = e * G                                      # 검증자는 공개키를 이미 알고 있다고 가정

        print("public_key: ",public_key)
        print("hex(z): ", hex(z))
        print("hex(r): ",hex(r))
        print("hex(s): ",hex(s))

    def exercise9(self):
        # [연습문제 3.7]
        print("********** [비밀키 e 로 메시지의 z 의 서명 구하기] **********")
        e = 12345
        z = int.from_bytes(hash256(b'Programming Bitcoin!'), 'big')
        k = 1234567890
        G = S256Point(GX, GY)
        k_inverse = pow(k, N-2, N)

        r = (k * G).x.num
        s = (z + r*e) * k_inverse % N
        print("hex(z): ", hex(z))
        print("hex(r): ", hex(r))
        print("hex(s): ", hex(s))




## 책 예제 테스트 코드 구현
run(S256Test("test_order"))             # 유한순환군의 N 인지 확인하는 기능 구현
run(S256Test("test_pubpoint"))          # 비밀키와 공개키 일치하는지 확인
run(S256Test("test_verify"))            # 전자 서명 검증 기능 테스트
run(S256Test("test_sec"))                 # 공개키 직렬화 sec 테스트
run(S256Test("test_address"))           # 비트코인 주소 테스트

# ## 비트코인에서 제안한 타원곡선 암호 및 전자서명 생성 및 검증 테스트
# run(S256Test("exercise1"))            # 생성점 G 가 y^2 = x^3 + 7 위에 있는지 확인
# run(S256Test("exercise2"))            # SECP256k1 곡선의 생성점 G로 생성한 군의 위수가 n 인지 확인
# run(S256Test("exercise3"))            # SECP256k1 곡선의 생성점 G로 생성한 군의 위수가 n 인지 확인 - config 변수 사용
# run(S256Test("exercise4"))            # secp256k1 에서 생성한 G 로 생성한 군의 위수가 n 이라는 것을 확인 하기
#
# run(S256Test("exercise5"))            # 서명 검증
# run(S256Test("exercise6"))            # 2개의 서명 검증하기
# run(S256Test("exercise7"))            # 2개의 서명 검증하기 - s256point 인 공캐키 클래스의 verify 로 검증
#
# run(S256Test("exercise8"))            # 서명 생성
# run(S256Test("exercise9"))            # 비밀키 e 로 메시지의 z 의 서명 구하기



