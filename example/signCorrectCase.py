from random import randint
import os
import sys
sys.path.append(os.path.abspath("/Users/SG/PycharmProjects/bitcoin/"))
from config import A, B, P, N, G
from lib.helper import hash256

## 서명 생성
e = int.from_bytes(hash256(b'gyu'), 'big') # 개인키 생성
z = int.from_bytes(hash256(b"gyu's message"), 'big') # 메시지 생성
k = randint(0, N) # k 는 랜덤 값

k_inverse = pow(k, N-2, N) # 1/k <- k 의 역수
r = (k*G).x.num # 목표값 x 좌표
s = (z+r*e)  * k_inverse % N

public_point = e * G # 공개키

## 서명 검증
s_inverse = pow(s, N-2, N)
u = z * s_inverse % N
v = r * s_inverse % N
R = u * G + v * public_point

if R.x.num == r:
    print("서명 생성 값과 서명 검증 값이 같습니다. -> 서명 검증 완료")
else:
    print("서명 생성 값과 서명 검증 값이 다릅니다. -> 서명 검증 실패")