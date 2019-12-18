from lib.helper import (little_endian_to_int, int_to_little_endian)
from src.script import Script


class TransactionOut:
    def __init__(self, amount, script_public_key):
        self.amount = amount
        self.script_public_key = script_public_key

    def __repr__(self):
        return f'\t{self.amount}:{self.script_public_key}'

    @classmethod
    def parse(cls, stream):
        """
        트랜잭션 output 값 읽어오기
        1. 비트코인 금액 (8byte), 리틀엔디언
        2. 잠금 스크립트 (가변정수)

        :param stream:
        :return:
        """

        amount = little_endian_to_int(stream.read(8))
        script_public_key = Script.parse(stream)
        return cls(amount, script_public_key)

    def serialize(self):
        """
        주어진 트랜잭션 출력을 직렬화 하기
        :return:
            bytes result: 직렬화된 트랜잭션 출력 객체
        """
        result = int_to_little_endian(self.amount, 8)    # 비트코인 금액을 byte 값으로
        result += self.script_public_key.serialize()    # 스크립트에서 구현한 직렬화 기능 사용
        return result


