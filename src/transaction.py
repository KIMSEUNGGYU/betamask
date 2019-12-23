from lib.helper import (hash256, little_endian_to_int, read_variant, int_to_little_endian, encode_variant, SIGNATURE_HASH_ALL)
from src.transactionIn import TransactionIn
from src.transactionOut import TransactionOut
from src.script import Script


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

    def signature_hash(self, input_index):
        """
        input_index에 서명해야하는 해시의 정수 표현을 리턴
        결국은 트랜잭션 값을 재정의해서 -> 서명 해시값 구하기 (z)

        input_index 와 연관 있는 트랜잭션 input 객체에 해제스크립트 대신에 잠금 스크립트 넣음
        1. 버전
        2. 입력 갯수
        3. 입력들
        4. 출력 갯수
        5. 출력들
        6. 락타임
        7. 해시 유형

        :param input_index:
        :return:
        """
        ## 1. 버전 구하기
        version = int_to_little_endian(self.version, 4)                         # 버전 구하기

        ## 2. 입력 연관
        inputs_number = encode_variant(len(self.tx_inputs))                     # 입력 갯수 구하기
        inputs = b''
        for i, tx_input in enumerate(self.tx_inputs):                           # 입력 트랜잭션 직렬화?
            if i == input_index:                                                # 내가 찾고하는 Index 라면 해제스크립트 자리에 잠금 스크립트 삽입
                # print('i == index')
                # script_signature = tx_input.script_public_key
                inputs += TransactionIn(
                    previous_transaction=tx_input.previous_transaction,         # 이전 트랜잭션
                    previous_index=tx_input.previous_index,                     # 이전 트랜잭션 index
                    script_signature=tx_input.script_public_key(testnet=True),  # 잠금스크립트 값 넣기 (얘가 핵심)
                    sequence=tx_input.sequence                                  # 입력 시퀀스 값 넣기
                ).serialize()
            else:                                                               # 내가 원하는 index 가 아니면, 해제스크립트 비워두기 ?
                # print('i !!= index')
                # script_signature = None
                inputs += TransactionIn(
                    previous_transaction=tx_input.previous_transaction,
                    previous_index=tx_input.previous_index,
                    sequence=tx_input.sequence
                ).serialize()

        ## 3. 출력 연관
        outputs_number = encode_variant(len(self.tx_outputs))   # 출력 갯수 구하기
        outputs = b''
        for tx_output in self.tx_outputs:
            outputs += tx_output.serialize()


        ## 4. 락타임
        locktime = int_to_little_endian(self.locktime, 4)

        ## 5. 해시 유형
        hash_type = int_to_little_endian(SIGNATURE_HASH_ALL, 4)

        result = version + inputs_number + inputs + outputs_number + outputs + locktime + hash_type
        hash256_value = hash256(result)
        return int.from_bytes(hash256_value, 'big')

    def verify_input(self, input_index):
        """
        트랜잭션 각각의 입력들 검증
        :param input_index:
        :return:
        """

        tx_input = self.tx_inputs[input_index]
        # print('tx_input', tx_input)
        script_public_key = tx_input.script_public_key(testnet=self.testnet)
        # print('&&script_public_key:', script_public_key)
        z = self.signature_hash(input_index=input_index)
        # print('z', z)

        # print('&&tx_input.script_signature:', tx_input.script_signature)

        combined_script = tx_input.script_signature + script_public_key         # 스크립트 값 확인해보기
        return combined_script.evaluate(z)

    def verify(self):
        """
        트랜잭션이 유효한지 검증
        :return:
        """
        """Verify this transaction"""
        if self.fee() < 0:                      # 수수료가 음수인지 확인 - 코인이 발행되지 않게 하기 위해
            return False

        for i in range(len(self.tx_inputs)):    # 각 입력이 올바른 해제 스크립트를 가지고 있는지 확인
            if not self.verify_input(i):
                print("input error")
                return False

        return True

    def signature_input(self, input_index, private_key, compressed=True):
        """
        해제스크립트 기능 
        :param input_index:
        :param private_key:
        :param compressed:
        :return:
        """
        z = self.signature_hash(input_index)
        der = private_key.sign(z).der()
        signature = der + SIGNATURE_HASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec(compressed=compressed)

        # print('tx_in', self.tx_inputs)
        self.tx_inputs[input_index].script_signature = Script([signature, sec])
        return self.verify_input(input_index)


