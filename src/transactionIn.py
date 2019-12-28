from lib.helper import (little_endian_to_int, int_to_little_endian)
from src.script import Script
# from src.api import (tx_fetch, utxo_fetcher)
# from src.transactionFetcher import TxFetcher
# from src.api import TxFetcher
from src.fetcher import Fetcher

class TransactionIn:
    def __init__(self, previous_transaction, previous_index, script_signature=None, sequence=0xffffffff):
        self.previous_transaction = previous_transaction
        self.previous_index = previous_index
        if script_signature is None:
            self.script_signature = Script()            # 그냥 빈 스크립트 객체를 반환
        else:
            self.script_signature = script_signature
        self.sequence = sequence

    def __repr__(self):
        return f'\t{self.previous_transaction.hex()}:{self.previous_index}'

    @classmethod
    def parse(cls, stream):
        """
        트랜잭션 input 값 읽어오기
        1. 이전 트랜잭션 id 값 (256bit -> 32byte), 리틀엔디언
        2. 이전 트랜잭션 인덱스 (4byte), 리틀엔디언
        3. 해제 스크립트 (가변정수)
        4. 시퀀스 (마지막 4byte)
        :param stream:
        :return:
        """

        previous_transaction = stream.read(32)[::-1]            # 1. 이전 트랜젹선 id 는 sha256 해시값 이므로 32byte, 리틀엔디언
        previous_index = little_endian_to_int(stream.read(4))   # 2. 4byte, 리틀엔디언
        script_signature = Script.parse(stream)                 # 3. 해제 스크립트는 길이가 변하는 필드, 가변길이 필드는 정확한 길이를 먼저 파싱해야함.
        sequence = little_endian_to_int(stream.read(4))         # 4. 시퀀스 필드, 리틀엔디언

        return cls(previous_transaction, previous_index, script_signature, sequence)

    def serialize(self):
        """
        주어진 트랜잭션 출력을 직렬화 하기
        :return:
            bytes result: 직렬화된 트랜잭션 출력 객체
        """
        result = self.previous_transaction[::-1]                    # 이전 트랜잭션 자체를 리틀엔디언 방식으로 읽기
        result += int_to_little_endian(self.previous_index, 4)      # 이전 트랜잭션 index를 직렬화하기
        result += self.script_signature.serialize()                 # script 클래스에 구현한 serialize 기능 사용
        result += int_to_little_endian(self.sequence, 4)            # 시퀀스 값 직렬화
        return result


    def fetch_tx(self, testnet=False):
        """
        UTXO? 기능을 하는 Txfetcher 를 이용해서 거래 기록? 가져오기
        :param testnet:
        :return:
        """
        # return TxFetcher.fetch(self.previous_transaction.hex(), testnet=testnet)
        return Fetcher.fetch(self.previous_transaction.hex(), testnet=testnet)
        # return TxFetcher.fetch(self.previous_transaction.hex())


    def value(self, testnet=False):
        """
        트랜잭션 해시값에서 출력값을 구함 - 출력값은 비트코인 보낼양
        :param testnet:
        :return:
        """
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outputs[self.previous_index].amount # ??

    def script_public_key(self, testnet=False):
        """
        트랜잭션 해시값에서 잠금 스크립트를 가져오는 기능
        :param testnet:
        :return:
        """
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outputs[self.previous_index].script_public_key



