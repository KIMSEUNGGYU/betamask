from unittest import TestSuite, TextTestRunner
import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

## TEST 실행
def run(test):
    suite = TestSuite()
    suite.addTest(test)
    TextTestRunner().run(suite)

## HASH
def hash256(str):
    '''sha256 두 번 반복'''
    return hashlib.sha256(hashlib.sha256(str).digest()).digest()

def hash160(str):
    '''sha256 -> ripemd160 수행'''
    return hashlib.new('ripemd160', hashlib.sha256(str).digest()).digest()


## BASE 58
def encode_base58(str):
    """
    임의 길이의 bytes 형 값을 받아 Base58로 부호화된 string 형 값을 반환
    :param str:
    :return:
    """
    ## p2pkh 에서 필요한 작업 수행 - 앞에 몇 byte가 0인지 기억했다가 -> 그 갯수만큼 1로 만듦
    count = 0
    for char in str:
        if char == 0:
            count += 1
        else:
            break

    num = int.from_bytes(str, 'big')
    prefix = '1' * count
    result = ''

    ## 58진수로 수 체계 생성 (BASE58 수체계)
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result

    return prefix + result


def encode_base58_checksum(b):
    """
    base58 로 부호화도 하고, 그 중간에 checksum도 넣고

    비트코인을 구하는 방식은
    1. 메인넷은 0x00 으로 시작, 테스트넷은 0x6f 로 시작
    2. sec 형식 주소를 hash160 방식을 사용해서 출력값을 얻음
    3. 1단계의 값과 2단계의 값을 합침
    4. 3에서 얻은 결과를 hash256 하고, 그 결과의 첫 4바이트 취함 <- checksum 구하기
    5. 3의 결과 뒤에 4의 결과를 붙이고 BASE58로 부호화

    가  있는데 그 중에서 4, 5 방식을 처리, 입력받은 파리미터 값이 3 단계의 값


    :param b: prefix(네트워크 종류) + sec 값 합친 값 - bytes 타입
    :return:
    """
    return encode_base58(b + hash256(b)[:4])


## 내가 안 짬
def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum, hash256(combined[:-4])[:4]))
    return combined[1:-4]



## 바이트 타입을 -> 정수형으로 반환 (리틀엔디언, 빅엔디언)
def little_endian_to_int(bytes):
    """
    byte 타입 값을 읽어서 리틀엔디언 정수로 반환
    :param bytes: 바이트 값
    :return:
    """
    return int.from_bytes(bytes, 'little')


def int_to_little_endian(n, length):
    """
    정수를 받아 리틀엔디언으로 bytes 형 값으로 반환
    :param n:       정수 n
    :param length:  bytes 갯수
    :return:
        bytes: 정수 n 의 리틀엔디언 방식 바이트값
    """
    return n.to_bytes(length, 'little')


# ## 가변 정수 파싱 및 직렬화 기능 구현
def read_variant(stream):
    """
    스트림으로부터 필요한 바이트 개수만큼 읽고 이를 정수로 반환함
    :param stream:
    :return:
        int: stream 정수 값
    """

    index = stream.read(1)[0]
    if index == 0xfd:
        # 0xfd 는 2byte 를 리틀엔디언으로 읽음
        return little_endian_to_int(stream.read(2))
    elif index == 0xfe:
        # 0xfe 는 4byte 를 리틀엔디언으로 읽음
        return little_endian_to_int(stream.read(4))
    elif index == 0xff:
        # 0xff 는 8byte 를 리틀엔디언으로 읽음
        return little_endian_to_int(stream.read(8))
    else:
        # anything else is just the integer ??
        return index

def encode_variant(integer_value):
    """
    정수값을 받아 variant 형식으로 변환된 bytes형 값을 반환함
    :param integer_value:
    :return:
        bytes: 정수값을 bytes 형태
    """
    if integer_value < 0xfd:
        return bytes([integer_value])
    elif integer_value < 0x10000: # 65536 pow(2, 16)-1
        return b'\xfd' + int_to_little_endian(integer_value, 2)
    elif integer_value < 0x100000000:
        return b'\xfe' + int_to_little_endian(integer_value, 4) # 4294967296, pow(2, 32)-1
    elif integer_value < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(integer_value, 8) # 18446744073709551616, pow(2, 64)-1
    else:
        raise ValueError(f'integer too large: {integer_value}')

