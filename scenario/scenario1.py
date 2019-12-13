from random import randint
import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))

from lib.config import (GX, GY, N)
from lib.helper import hash256
from src.s256Point import S256Point
from src.privatekey import PrivateKey

## 생성점 G 정의
G = S256Point(GX, GY)

def scenario1():
    ## 서명 생성
    e = int.from_bytes(hash256(b'gyu'), 'big') # 개인키 생성
    z = int.from_bytes(hash256(b"gyu's message"), 'big') # 메시지 생성
    k = randint(0, N) # k 는 랜덤 값

    k_inverse = pow(k, N-2, N) # 1/k <- k 의 역수
    r = (k*G).x.num # 목표값 x 좌표
    s = (z+r*e)  * k_inverse % N

    public_point = e * G # 공개키

    ### 잘못된 경우 - 개인키를 중간에 바꿈
    # e = int.from_bytes(hash256(b'hacking'), 'big') # 개인키 생성
    # r = (k*G).x.num # 목표값 x 좌표
    # s = (z+r*e)  * k_inverse % N


    ## 서명 검증
    s_inverse = pow(s, N-2, N)
    u = z * s_inverse % N
    v = r * s_inverse % N
    R = u * G + v * public_point

    if R.x.num == r:
        print("서명 생성 값과 서명 검증 값이 같습니다. -> 서명 검증 완료")
    else:
        print("서명 생성 값과 서명 검증 값이 다릅니다. -> 서명 검증 실패")


def scenario2():
    e = int.from_bytes(hash256(b'gyu'), 'big')
    z = int.from_bytes(hash256(b"gyu's message"), 'big') # 메시지 생성

    private_key = PrivateKey(e)
    signature =  private_key.sign(z)

    # 올바르지 않은 경우 - 개인키를 바꾸고 서명을 생성??
    # e = int.from_bytes(hash256(b'hacking'), 'big')
    # private_key = PrivateKey(e)

    print("서명 검증 결과: ", private_key.point.verify(z, signature))


# scenario1() # 클래스 사용하지 않고 raw 로직 그대로 한 것!
scenario2() # 클래스에 정의된 기능 사용한 것