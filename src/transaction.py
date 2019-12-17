from lib.helper import (hash256, little_endian_to_int, read_variant, int_to_little_endian, encode_variant)
from src.transactionIn import TransactionIn
from src.transactionOut import TransactionOut

class Transaction:
    def __init__(self, version, tx_inputs, tx_outputs, locktime, testnet=False):
        self.version = version
        self.tx_inputs = tx_inputs
        self.tx_outputs = tx_outputs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_inputs = ''
        for tx_input in self.tx_inputs:
            tx_inputs += tx_input.__repr__() + '\n'

        tx_outputs = ''
        for tx_output in self.tx_outputs:
            tx_outputs += tx_output.__repr__() + '\n'

        return f'transaction: {self.id()}\n' \
            f'version: {self.version}\n' \
            f'transaction_inputs: {tx_inputs}' \
            f'transaction_outputs: {tx_outputs}' \
            f'locktime: {self.locktime}'

    def id(self):
        """
        트랜잭션 자체를 hash256 해시 함수에 넣어 얻은 해시값을 16진수 형식으로 반환한 값
        :return:
        """
        return self.hash().hex()

    def hash(self):
        """
        트랜잭션 자체를 hash256 해시 함수에 넣은 해시 값을 반환
        1. serialize() 함수로 직렬화하고
        2. [::-1] 리틀엔디언 방식으로 읽기
        :return:
        """
        return hash256(self.serialize())[::-1]

    @classmethod
    def parse(cls, stream, testnet=False):
        """
        transaction 전체 파싱하는 것!
        1. 버전
        2. transaction inputs
        3. transaction outputs
        4. locktime

        ## 순서
        - 버전
        1. 버전은 첫 바이트 4바이트 읽음
        - 트랜잭션 입력들
        2. 입력의 갯수를 알기위해 read_variant 로 읽음 (가변정수)
        3. 입력의 갯수만큼 트랜잭션 입력(부분)을 파싱하고 각각의 트랜잭션 입력을 배열에 추가함 (inputs)
        - 트랜잭션 출력들
        4. 출력의 갯수를 알기 위해 read_variant 로 읽음 (가변정수)
        5. 출력의 갯수만큼 트랜잭션 출력(부분)을 파싱하고 각각의 트랜잭션 출력을 배열에 추가함
        - locktime
        6. 4바이트, 리틀엔디언

        :param stream:
            bytes array?: 스트림 값(트랜잭션 값)
        :param testnet:
            boolean: 테스트넷인지 아닌지
        :return:
        """

        # version
        version = little_endian_to_int(stream.read(4))  # 1단계 - 버전을 읽음
        ## 이렇게 한 번에 처리해야함!! stream 으로 오기 때문에??


        # transaction_inputs
        number_inputs = read_variant(stream)            # 2단계 - 트랜잭션_inputs(입력들) 의 갯수를 읽음
        transaction_inputs = []
        for _ in range(number_inputs):                  # 3단계 - 입력의 갯수만큼 트랜잭션 입력을 파싱함
            transaction_inputs.append(TransactionIn.parse(stream))

        # transaction_outputs
        number_outputs = read_variant(stream)           # 4단계 - 트랜잭션_outputs(출력들) 의 갯수를 읽음
        transaction_outputs = []
        for _ in range(number_outputs):                 # 5단계 - 출력의 갯수만큼 트랜잭션 출력을 파싱함
            transaction_outputs.append(TransactionOut.parse(stream))

        locktime = little_endian_to_int(stream.read(4)) # 6단계 - locktime 읽음, 4바이트, 리틀엔디언

        return cls(version, transaction_inputs, transaction_outputs, locktime, testnet=testnet)

    def serialize(self):
        """
        주어진 트랜잭션 직렬화 하기
        :return:
            bytes result: 직렬화된 트랜잭션 객체
        """
        result = int_to_little_endian(self.version, 4)      # 버전
        result += encode_variant(len(self.tx_inputs))       # 트랜잭션 입력 갯수, 가변정수
        for tx_input in self.tx_inputs:                     # 트랜잭션 입력 직렬화
            result += tx_input.serialize()
        result += encode_variant(len(self.tx_outputs))      # 트랜잭션 출력 갯수, 가변정수
        for tx_output in self.tx_outputs:                   # 트랜잭션 출력 직렬화
            result += tx_output.serialize()
        result += int_to_little_endian(self.locktime, 4)    # locktime 직렬화
        return result

    def fee(self):
        """
        트랜잭션의 수수료를 반환, 단위는 사토시 (1/1억)
        :return:
        """

        input_sum, output_sum = 0, 0
        # use TxIn.value() to sum up the input amounts
        for tx_in in self.tx_inputs:
            input_sum += tx_in.value(self.testnet)
        # use TxOut.amount to sum up the output amounts
        for tx_out in self.tx_outputs:
            output_sum += tx_out.amount
        # fee is input sum - output sum
        return input_sum - output_sum


