import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
import requests
from unittest import TestCase
from io import BytesIO

from lib.helper import (run, little_endian_to_int)
from src.transaction import Transaction
from src.script import Script

class TransactionTest(TestCase):
    # cache_file = '../tx.cache'
    @classmethod
    def setUpClass(cls):
        # fill with cache so we don't have to be online to run these tests
        pass
        # TxFetcher.load_cache(cls.cache_file)

    def test_parse_version(self):
        print("********** [트랜잭션 버전 parse 테스트] **********")
        raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_tx)
        tx = Transaction.parse(stream)
        self.assertEqual(tx.version, 1)

    def test_parse_inputs(self):
        print("********** [트랜잭션 inputs parse 테스트] **********")
        raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_tx)
        tx = Transaction.parse(stream)
        # print("tx:", tx)
        self.assertEqual(len(tx.tx_inputs), 1)

        want = bytes.fromhex('d1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81')
        self.assertEqual(tx.tx_inputs[0].previous_transaction, want)
        self.assertEqual(tx.tx_inputs[0].previous_index, 0)
        want = bytes.fromhex('6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        self.assertEqual(tx.tx_inputs[0].script_signature.serialize(), want)
        self.assertEqual(tx.tx_inputs[0].sequence, 0xfffffffe)

    def test_parse_outputs(self):
        print("********** [트랜잭션 outputs parse 테스트] **********")
        raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_tx)
        tx = Transaction.parse(stream)
        self.assertEqual(len(tx.tx_outputs), 2)
        want = 32454049
        self.assertEqual(tx.tx_outputs[0].amount, want)
        want = bytes.fromhex('1976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac')
        self.assertEqual(tx.tx_outputs[0].script_public_key.serialize(), want)
        want = 10011545
        self.assertEqual(tx.tx_outputs[1].amount, want)
        want = bytes.fromhex('1976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac')
        self.assertEqual(tx.tx_outputs[1].script_public_key.serialize(), want)

    def test_parse_locktime(self):
        print("********** [트랜잭션 locktime parse 테스트] **********")
        raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_tx)
        tx = Transaction.parse(stream)
        self.assertEqual(tx.locktime, 410393)

    def test_fee(self):
        print("********** [트랜잭션 fee parse 테스트] **********")
        raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_tx)
        tx = Transaction.parse(stream)
        self.assertEqual(tx.fee(), 40000)

        raw_tx = bytes.fromhex('010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600')
        stream = BytesIO(raw_tx)
        tx = Transaction.parse(stream)
        self.assertEqual(tx.fee(), 140500)

    def exercise1(self):
        #[연습문제 5.1]
        print("********** [트랜잭션 값, 버전만 parsing 하기] **********")
        raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')

        stream = BytesIO(raw_tx) # 바이트 배열을 이진 파일로 다룰 수 있게 해줌
        # print('stream 값: ', stream.getvalue())
        print("version: ", Transaction.parse(stream=stream))

    def exercise2(self):
        print("********** [byte 값을 정수로 변환하는 예제] **********")
        byte = bytes([11])
        print('data:', byte)
        print('little_to_int:', int.from_bytes(byte, 'little'))

    def exercise3(self):
        print("********** [스크립트는 6장에서 배우지만 간단하게 맛보기] - 스크립트 파싱 **********")
        script_hex = ('6b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        stream = BytesIO(bytes.fromhex(script_hex))
        script_signature = Script.parse(stream)
        print("해제 스크립트: ", script_signature)

    def exercise4(self):
        print("********** [트랜잭션 필드 값 찾기] **********")
        hex_transaction = '010000000456919960ac691763688d3d3bcea9ad6ecaf875df5339e148a1fc61c6ed7a069e010000006a47304402204585bcdef85e6b1c6af5c2669d4830ff86e42dd205c0e089bc2a821657e951c002201024a10366077f87d6bce1f7100ad8cfa8a064b39d4e8fe4ea13a7b71aa8180f012102f0da57e85eec2934a82a585ea337ce2f4998b50ae699dd79f5880e253dafafb7feffffffeb8f51f4038dc17e6313cf831d4f02281c2a468bde0fafd37f1bf882729e7fd3000000006a47304402207899531a52d59a6de200179928ca900254a36b8dff8bb75f5f5d71b1cdc26125022008b422690b8461cb52c3cc30330b23d574351872b7c361e9aae3649071c1a7160121035d5c93d9ac96881f19ba1f686f15f009ded7c62efe85a872e6a19b43c15a2937feffffff567bf40595119d1bb8a3037c356efd56170b64cbcc160fb028fa10704b45d775000000006a47304402204c7c7818424c7f7911da6cddc59655a70af1cb5eaf17c69dadbfc74ffa0b662f02207599e08bc8023693ad4e9527dc42c34210f7a7d1d1ddfc8492b654a11e7620a0012102158b46fbdff65d0172b7989aec8850aa0dae49abfb84c81ae6e5b251a58ace5cfeffffffd63a5e6c16e620f86f375925b21cabaf736c779f88fd04dcad51d26690f7f345010000006a47304402200633ea0d3314bea0d95b3cd8dadb2ef79ea8331ffe1e61f762c0f6daea0fabde022029f23b3e9c30f080446150b23852028751635dcee2be669c2a1686a4b5edf304012103ffd6f4a67e94aba353a00882e563ff2722eb4cff0ad6006e86ee20dfe7520d55feffffff0251430f00000000001976a914ab0c0b2e98b1ab6dbf67d4750b0a56244948a87988ac005a6202000000001976a9143c82d7df364eb6c75be8c80df2b3eda8db57397088ac46430600'
        # print("hex_transaction: ", hex_transaction)
        stream = BytesIO(bytes.fromhex(hex_transaction))        # 1. hex값을 byte[] 값 스트림으로 만든다.
        # print("stream:", stream.getvalue())
        transaction_object = Transaction.parse(stream=stream)   # 2. stream 값을 파싱한다.
        # 2.1 버전
        # 2.2 트랜잭션 inputs
        # 2.3 트랜잭션 outputs
        # 2.4 locktime

        print(f'두 번째 입력의 해제 스크립트: {transaction_object.tx_inputs[1].script_signature}')
        print(f'첫 번째 출력의 잠금 스크립트: {transaction_object.tx_outputs[0].script_public_key}')
        print(f'두 번째 출력의 비트코인 금액: {transaction_object.tx_outputs[1].amount}')


    def exercise5(self):
        print("********** [실제 트랜잭션 값 파싱 및 수수료 파싱하기 ] **********")

        # 필요한 데이터 설정
        transaction_id = 'f968c4b682f051ee5971df4196cc250be90e0dd828269eff9b3bb6201b238ddc'
        main_net = 'http://mainnet.programmingbitcoin.com'
        test_net = 'http://testnet.programmingbitcoin.com'
        url = '{}/tx/{}.hex'.format(main_net, transaction_id)

        ## 트랜잭션 파싱 수행?
        response = requests.get(url)    # response.text 는 트랜잭션 hex 값이 나옴
        try:
            transaction_raw = bytes.fromhex(response.text.strip())
        except ValueError:
            raise ValueError(f'unexpected response: {response.text}')


        print(len(transaction_raw))
        if transaction_raw[4] == 0:
            transaction_raw = transaction_raw[:4] + transaction_raw[6:]                 # transaction_raw 의 5번째 요소 제외함
            transaction = Transaction.parse(BytesIO(transaction_raw), testnet=False)    # 메인넷 데이터 파싱
            transaction.locktime = little_endian_to_int(transaction_raw[-4:])           # 마지막 4바이트 값을 locktime 으로
        else:
            transaction = Transaction.parse(BytesIO(transaction_raw), testnet=False)

        if transaction.id() != transaction_id:
            raise ValueError(f'파싱한 트션랜잭션 값{transaction.id()} 과 입력받은 트랜잭션 {transaction_id} 가 같지 않습니다.')

        print("트랜잭션 값: ")
        print(transaction)
        print("입력 트랜잭션 값:")
        print(transaction.tx_inputs)
        print("수수료 값:", transaction.fee())


# url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)





## 테스트 코드 실행
# run(TransactionTest("test_parse_version"))      # 트랜잭션 버전 parse 테스트
# run(TransactionTest("test_parse_inputs"))       # 트랜잭션 inputs parse 테스트
# run(TransactionTest("test_parse_outputs"))      # 트랜잭션 outputs parse 테스트
# run(TransactionTest("test_parse_locktime"))     # 트랜잭션 lokctime parse 테스트
# run(TransactionTest("test_fee"))                # 트랜잭션 수수료 테스트




## 책 예제 테스트 코드 실행
# run(TransactionTest("exercise1"))       # 트랜잭션 값, 버전만 parsing 하기
# run(TransactionTest("exercise2"))       # byte 값을 정수로 변환하는 예제
# run(TransactionTest("exercise3"))       # 스크립트 파싱
# run(TransactionTest("exercise4"))       # 트랜잭션 필드 값 찾기
run(TransactionTest("exercise5"))       # 트랜잭션 필드 값 찾기



