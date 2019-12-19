from logging import getLogger

from lib.helper import (read_variant, encode_variant, little_endian_to_int, int_to_little_endian)
from src.op import (OP_CODE_FUNCTIONS, OP_CODE_NAMES)

LOGGER = getLogger(__name__)

class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds            # 명령어를 실행할 공간으로 연산자 와 피연산자로 구성

    @classmethod
    def parse(cls, stream):
        """
        스크립트 값인 bytes 값을 받아 Script 객체로 생성
        :param stream:
            bytes: 스크립트 값, 바이트 타입
        :return:
        """
        length = read_variant(stream)   # 전체 스크립트의 길이를 읽음 (이싱후에 count 와 비교하기 위해서 - 스크립트 길이만 파싱하기 위함 )
        cmds = []
        count = 0

        while count < length:           # 정확히 스크립트 길이만큼만 파싱하기 위해서
            current = stream.read(1)    # 1 byte 파싱 - 원소인지? 연산자 인지? 판단하기 위해서
            count += 1
            current_byte = current[0]   # bytes 값을 정수형으로 변환
            if current_byte >= 1 and current_byte <= 75:                #  1 ~ 75 범위라면 다음 n byte 가 하나의 원소
                n = current_byte
                cmds.append(stream.read(n))
                count += n
            elif current_byte == 76:                                    # 76은 OP_PUSHDATA1 을 의미 - 1 byte 를 더 읽어 파싱할 원소의 길이를 얻어야 함
                data_length = little_endian_to_int(stream.read(1))      # 1 byte 더 읽음
                cmds.append(stream.read(data_length))
                count += data_length + 1
            elif current_byte == 77:                                    # 77은 OP_PUSHDATA2 를 의미 - 2 byte 를 더 읽어 파싱할 원소의 길이를 얻어야 함
                data_length = little_endian_to_int(stream.read(2))      # 2 byte 더 읽음
                cmds.append(stream.read(data_length))
                count += data_length + 2
            else:
                op_code = current_byte                                  # 해당 경우에는 OP_CODE 가 됨
                cmds.append(op_code)

        if count != length:                                             # 처음 스크립트 길이만큼 스크립트 파싱이 이루어졌는지 확인
            raise SyntaxError('parsing script failed')

        return cls(cmds)

    def raw_serialize(self):
        """
        스크리트 직렬화 값 구하기
        스크립트 객체를 bytes 값으로 변환음
        :return:
        """
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:                                # 명령어가 정수값이면 연산자를 의미함
                result += int_to_little_endian(cmd, 1)          ## cmd 라는 값을 1 byte 리틀엔디언으로 변환, 얘가 OP 코드 같음
            else:
                length = len(cmd)                               ## 이부분이 피연산자 같음
                if length <= 75:                                # 길이가 1 ~ 75 범위라면, 그 길이를 1 byte로 표현
                    result += int_to_little_endian(length, 1)
                elif length > 75 and length < 0x100:            # 길이가 76 ~ 255 범위라면, OP_PUSHDATA1 를 넣어주고, 1byte로 리틀엔디언으로 길이를 표현
                    result += int_to_little_endian(76, 1)       ## OP_PUSHDATA1 의 키워드를 넣어주고
                    result += int_to_little_endian(length, 1)   ## 길이 넣기 ? <- 무슨 길이지??
                elif length >= 0x100 and length <= 520:         # 길이가 256 ~ 520 범위라면, OP_PUSHDATA2 를 넣어주고, 2byte 리틀엔디언으로 길이를 표현
                    result += int_to_little_endian(77, 1)       ## OP_PUSHDATA2 의 키워드를 넣어주고
                    result += int_to_little_endian(length, 2)   ## 길이 넣기 <- 무슨 길이?
                else:                                           # 520 보다 긴 원소는 직렬화 불가능
                    raise ValueError('too long an cmd')

                result += cmd
        return result

    def serialize(self):
        """
        스크립트는 "스크립트직렬화길이" 와 "스크립트직렬화값" 으로 구성되어있
        :return:
        """
        result = self.raw_serialize()
        total = len(result)
        return encode_variant(total) + result                   # 직렬화된 스크립트 길이 + 직렬화된 스크립트

    def __add__(self, other):
        """
        잠금 스크립트와 해제 스크립트를 결합시키는 코
        :param other:
        :return:
        """
        return Script(self.cmds + other.cmds)
    # def __add___(self, other):
    #     """
    #     잠금 스크립트와 해제 스크립트를 결합시키는 코
    #     :param other:드
    #     :return:
    #     """
    #     return Script(self.cmds + other.cmds)       # 두 스크립트(잠금, 해제) 를 합하여 스크립트 객체 생성

    def evaluate(self, z):
        """

        - 실제 스택 구조 처럼 사용하지 않는 거 같음 LIFO 방식인데... 배열로 구성했을 때 마지막 원소가 아닌, 맨 첫번째 원소부터 뺌
        :param z:
        :return:
        """
        cmds = self.cmds[:]             # 전체 복사
        stack = []
        altstack = []

        while len(cmds) > 0:
            cmd = cmds.pop(0)           # 스택의 맨 첫번째 요소, 맨 왼쪽 요소 꺼냄

            if type(cmd) == int:        # 연산자 - cmd 가 정수면 연산자
                operation = OP_CODE_FUNCTIONS[cmd]                      # op코드에 해당하는 연산자

                if cmd in (99, 100):                                    # 99와 100인 경우 - OP_IF 와 OP_NOTIF 연산자
                    if not operation(stack, cmds):
                        LOGGER.info(f'bad op: {OP_CODE_NAMES[cmd]}')
                        return False
                elif cmd in (107, 108):                                 # 107, 108인 경우 - OP_TOALTSTAK, OP_FROMALTSTAK 연산자
                    if not operation(stack, altstack):
                        LOGGER.info(f'bad op: {OP_CODE_NAMES[cmd]}')
                        return False
                elif cmd in (172, 173, 174, 175):
                    # 172, 173, 174, 175인 경우 - OP_CHECKSIG, OP_CHECKSIGVERIFY, OP_CHECKMULTISIG, OP_CHECKMULTISIGVERIFY
                    if not operation(stack, z):
                        LOGGER.info(f'bad op: {OP_CODE_NAMES[cmd]}')
                        return False
                else:                   # 피연산자(원소) - 명령어가 원소
                    if not operation(stack):
                        LOGGER.info(f'bad op: {OP_CODE_NAMES[cmd]}')
                        return False
            else:                       # 엘리먼트(요소)
                stack.append(cmd)

        if len(stack) == 0:             # 모든 명령어를 실행 후, 스택이 비어있으면 스크립트 유효성 실패
            return False

        if stack.pop() == b'':          # 최상위 요소가 0 인경우 - 공 바이트(b'')
            return False

        return True                     # 스크립트 유효한 경우

