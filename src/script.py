from lib.helper import (read_variant, encode_variant, little_endian_to_int, int_to_little_endian)

class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds            # 명령어를 실행할 공간으로 연산자 와 피연산자로 구성

    @classmethod
    def parse(cls, stream):
        print("script2")
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





