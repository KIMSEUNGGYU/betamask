from io import BytesIO

class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

    def der(self):
        """
        서명 직렬화
        (r, s) 모두 직렬화함.
        압축하지 못함. 왜냐하면 s 값을 r 값 만으로 유도할 수 없음
        1. 0x30 바이트로 시작
        2. 서명의 길이 붙임
        3. r 값의 시작을 표시하는 0x02 붙임
        4. r 값의 길이 붙임
        5. r 값 붙임. 이때 첫 비트가 1 이상인 경우 앞에 00을 붙임 즉, [00] + r 값
        6. s 값의 시작을 표시하는 0x02 붙임
        7. s 값의 길이 붙임
        8. s 값 붙임. 이때 첫 비트가 1 이상인 경우 앞에 00을 붙임 즉, [00] + s 값

        :return:
        """


        ## r 값 직렬화
        r_binary = self.r.to_bytes(32, byteorder='big')
        # 처음 시작 부분에 null 이 있는 부분 없애기
        r_binary = r_binary.lstrip(b'\x00')             # 왼쪽에 b'00' 이 있으면 해당 부분 제거

        # der 은 양수/음수 모두 가능하지만, ECDSA 는 양수만 있기 때문에 첫 비트가 1 이상인 수가 나와면 앞에 00 값을 붙임
        if r_binary[0] & 0x80:
            r_binary = b'\x00' + r_binary               # 5 단계

        # 3. 정수 2 와 len(r_binary) 인 값을 바이트 형태로 만듦 + r_binary 값
        result = bytes([2, len(r_binary)]) + r_binary   # 3, 4 단계 + 5 단계

        ## s 값 직렬화
        s_binary = self.s.to_bytes(32, byteorder='big')
        s_binary = s_binary.lstrip(b'\x00')

        if s_binary[0] & 0x80:
            s_binary = b'\x00' + s_binary               # 8 단계

        result += bytes([2, len(s_binary)]) + s_binary  # 6, 7, 8
        return bytes([0x30, len(result)]) + result

    ## 정리 해야함
    @classmethod
    def parse(cls, signature_bin):
        """
        서명 직렬화된 값(der) 을 다시 원래의 서명값으로 되돌리기
        :param signature_bin: der 로 직렬화된 값
        :return:
        """
        s = BytesIO(signature_bin)
        compound = s.read(1)[0]
        if compound != 0x30:
            raise SyntaxError("Bad Signature")
        length = s.read(1)[0]
        if length + 2 != len(signature_bin):
            raise SyntaxError("Bad Signature Length")
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        rlength = s.read(1)[0]
        r = int.from_bytes(s.read(rlength), 'big')
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        slength = s.read(1)[0]
        s = int.from_bytes(s.read(slength), 'big')
        if len(signature_bin) != 6 + rlength + slength:
            raise SyntaxError("Signature too long")
        return cls(r, s)