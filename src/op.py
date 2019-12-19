
from logging import getLogger

from lib.helper import (hash256, hash160)
from src.s256Point import S256Point
from src.signature import Signature

LOGGER = getLogger(__name__)

"""
OP 를 위한 라이브러리
"""
def encode_num(number):
    """
    정수형 숫자 값을 byte 로 변환
    :param number:
    :return:
    """
    if number == 0:
        return b''

    abs_number = abs(number)
    negative = number < 0
    result = bytearray()

    while abs_number:
        result.append(abs_number & 0xff)    # 0xff = 255
        abs_number >>= 8                    # 8byte 씩 shift

    if result[-1] & 0x80:                   # 0x80 = 128
        if negative:
            result.append(0x80)
        else:
            result.append(0)
    elif negative:
        result[-1] |= 0x80

    return bytes(result)

def decode_num(element):
    """
    바이트 element 를 정수로 변환

    - 첫 바이트가 1 인 경우 음수로 판단해 그 부분을 처리 및 정수값 추출
    :param element:
    :return:
    """
    if element == b'':
        return 0

    big_endian = element[::-1]      # 전체 복사

    ## 음수인지 체크 - 첫 byte 로 검사
    if big_endian[0] & 0x80:
        negative = True
        result = big_endian[0] & 0x7f
    else:
        negative = False
        result = big_endian[0]

    ## 이후 데이터로 정수값 얻기
    for ch in big_endian[1:]:
        result <<= 8
        result += ch

    ## 첫바이트가 1인 경우 (음수로인식하는 것을 막기위함?) - 붙여 정수로 표현?
    if negative:
        return -result
    else:
        return result




"""
OP 기능
"""
def op_duplicate(stack):
    """
    원소를 복사하는 기능
    :param stack:
    :return:
    """
    if len(stack) < 1:          # 스택에 원소가 하나라도 있어야 복사 가능
        return False

    stack.append(stack[-1])     # 스택의 최상위 요소를 복사하는 기능
    return True

def op_hash256(stack):
    """
    스택 최상위 요소 값을 hash256 해시 값으로 만들기
    :param stack:
    :return:
    """
    if len(stack) < 1:
        return False

    element = stack.pop()
    hash256_value = hash256(element)
    stack.append(hash256_value)
    return True

def op_hash160(stack):
    """
    스택 최상위 요소 값을 hash256 해시 값으로 만들기
    :param stack:
    :return:
    """
    if len(stack) < 1:
        return False

    element = stack.pop()
    hash160_value = hash160(element)
    stack.append(hash160_value)
    return True

def op_checksignature(stack, z):
    """
    서명 검사 연산 수행
    :param stack:   스택
    :param z:   서명 해시?
    :return:
    """
    if len(stack) < 2:
        return False

    sec_public_key = stack.pop()            # 1. 공개키 값
    der_signature = stack.pop()[:-1]        # der 서명에서 마지막 값을 빼는데 왜빼지??   # 2. 서명 값

    try:
        public_key = S256Point.parse(sec_public_key)
        signature = Signature.parse(der_signature)
    except (ValueError, SyntaxError) as error:
        return False

    ## 검증 부분?
    if public_key.verify(z, signature):
        stack.append(encode_num(1))
    else:
        stack.append(encode_num(0))

    return True


"""
op 피연산자
"""
def op_0(stack):
    stack.append(encode_num(0))
    return True


"""
OP 함수 정의
"""
OP_CODE_FUNCTIONS = {
    0: op_0,
    118: op_duplicate,          # 118 = 0x76
    169: op_hash160,            # 169 = 0xa9
    170: op_hash256,            # 170 = 0xaa
    172: op_checksignature,     # 172 = 0xac
}

OP_CODE_NAMES = {
    0: 'OP_0',
    118: 'OP_DUP',
    169: 'OP_HASH160',
    170: 'OP_HASH256',
    172: 'OP_CHECKSIG',
}
