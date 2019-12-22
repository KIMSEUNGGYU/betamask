import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
import requests
from unittest import TestCase
from io import BytesIO

from lib.helper import (run, little_endian_to_int, hash256, decode_base58, SIGNATURE_HASH_ALL)
from src.transaction import Transaction
from src.transactionIn import TransactionIn
from src.transactionOut import TransactionOut
from src.script import (Script, p2pkh_script)
from src.s256Point import S256Point
from src.signature import Signature
from src.privatekey import PrivateKey

# from src.transactionFetcher import TxFetcher
from src.transactionFetcher import TxFetcher2


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

    def test_serialize(self):
        print("********** [트랜잭션 직렬화 테스트] **********")
        raw_tx = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(raw_tx)
        tx = Transaction.parse(stream)
        self.assertEqual(tx.serialize(), raw_tx)

    def test_input_value(self):
        print("********** [트랜잭션 입력의 출력값 구하기] **********")
        tx_hash = 'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81'
        index = 0
        want = 42505594
        tx_in = TransactionIn(bytes.fromhex(tx_hash), index)
        print('트랜잭션 입력의 출력값:', tx_in.value())
        self.assertEqual(tx_in.value(), want)

    def test_input_pubkey(self):
        print("********** [트랜잭션 잠금 스크립트 구하기] **********")
        tx_hash = 'd1c789a9c60383bf715f3f6ad9d14b91fe55f3deb369fe5d9280cb1a01793f81'
        index = 0
        tx_in = TransactionIn(bytes.fromhex(tx_hash), index)
        want = bytes.fromhex('1976a914a802fc56c704ce87c42d7c92eb75e7896bdc41ae88ac')
        print("트랜잭션 잠금 스크립트: ", tx_in.script_public_key())
        self.assertEqual(tx_in.script_public_key().serialize(), want)

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


    # 추가해야함 테스트 코드
    def test_sig_hash(self):
        print("********** [트랜잭션 서명 해시 구하는 방법?] **********")
        tx = TxFetcher.fetch('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03')
        # want = int('27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6', 16)
        # self.assertEqual(tx.signature_hash(0), want)

    def test_sig_hash2(self):
        print("********** [트랜잭션 서명 해시 구하는 방법 22222] **********")
        tx = TxFetcher2.fetch('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03', testnet=False)
        want = int('27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6', 16)
        self.assertEqual(tx.signature_hash(0), want)


    def test_verify_p2pkh(self):
        """ 테스트넷은 에러가 남 """
        print("********** [트랜잭션 p2pkh 서명 검증?] **********")
        tx = TxFetcher.fetch('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03')
        self.assertTrue(tx.verify())
        # tx = TxFetcher.fetch('5418099cc755cb9dd3ebc6cf1a7888ad53a1a3beb5a025bce89eb1bf7f1650a2', testnet=True)
        # self.assertTrue(tx.verify())

    def test_verify_p2pkh2(self):
        """ 테스트넷은 에러가 남 """
        print("********** [트랜잭션 p2pkh 서명 검증? 2222] **********")
        tx = TxFetcher2.fetch('452c629d67e41baec3ac6f04fe744b4b9617f8f859c63b3002f8684e7a4fee03')
        self.assertTrue(tx.verify())


    def test_verify_p2sh(self):
        tx = TxFetcher.fetch('46df1a9484d0a81d03ce0ee543ab6e1a23ed06175c104a178268fad381216c2b')
        self.assertTrue(tx.verify())

    def test_verify_p2sh2(self):
        print("********** [ 2222 ] **********")
        tx = TxFetcher2.fetch('46df1a9484d0a81d03ce0ee543ab6e1a23ed06175c104a178268fad381216c2b')
        self.assertTrue(tx.verify())

    def test_sign_input(self):      # 잘안됨
        pass
        # private_key = PrivateKey(secret=8675309)
        # stream = BytesIO(bytes.fromhex('010000000199a24308080ab26e6fb65c4eccfadf76749bb5bfa8cb08f291320b3c21e56f0d0d00000000ffffffff02408af701000000001976a914d52ad7ca9b3d096a38e752c2018e6fbc40cdf26f88ac80969800000000001976a914507b27411ccf7f16f10297de6cef3f291623eddf88ac00000000'))
        # tx_obj = Transaction.parse(stream, testnet=True)
        # self.assertTrue(tx_obj.signature_input(0, private_key))
        # want = '010000000199a24308080ab26e6fb65c4eccfadf76749bb5bfa8cb08f291320b3c21e56f0d0d0000006b4830450221008ed46aa2cf12d6d81065bfabe903670165b538f65ee9a3385e6327d80c66d3b502203124f804410527497329ec4715e18558082d489b218677bd029e7fa306a72236012103935581e52c354cd2f484fe8ed83af7a3097005b2f9c60bff71d35bd795f54b67ffffffff02408af701000000001976a914d52ad7ca9b3d096a38e752c2018e6fbc40cdf26f88ac80969800000000001976a914507b27411ccf7f16f10297de6cef3f291623eddf88ac00000000'
        # self.assertEqual(tx_obj.serialize().hex(), want)  #


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

    def exercise6(self):
        print("********** [트랜잭션 직렬화 ] **********")
        # 필요한 데이터 설정
        transaction_id = 'a3cce92d4e81de7bb1829dd3e78162c6359f88ae5149f8f6d843d9fe92d1fcbc'
        main_net = 'http://mainnet.programmingbitcoin.com'
        test_net = 'http://testnet.programmingbitcoin.com'
        url = '{}/tx/{}.hex'.format(main_net, transaction_id)

        print("트랜잭션 raw data")
        response = requests.get(url)
        try:
            transaction_raw = bytes.fromhex(response.text.strip())
        except ValueError:
            raise ValueError(f'unexpected response: {response.text}')

        print(transaction_raw.hex())
        if transaction_raw[4] == 0:
            transaction_raw = transaction_raw[:4] + transaction_raw[6:]                 # transaction_raw 의 5번째 요소 제외함
            transaction = Transaction.parse(BytesIO(transaction_raw), testnet=False)    # 메인넷 데이터 파싱
            transaction.locktime = little_endian_to_int(transaction_raw[-4:])           # 마지막 4바이트 값을 locktime 으로
        else:
            transaction = Transaction.parse(BytesIO(transaction_raw), testnet=False)

        if transaction.id() != transaction_id:
            raise ValueError(f'파싱한 트션랜잭션 값{transaction.id()} 과 입력받은 트랜잭션 {transaction_id} 가 같지 않습니다.')

        print("트랜잭션 직렬화:")
        print(transaction.serialize().hex())

    def exercise7(self):
        print("********** [ 트랜잭션 수수료 검증 ] **********")
        raw_transaction = ('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(bytes.fromhex(raw_transaction))
        transaction = Transaction.parse(stream)
        # print('transaction', transaction)
        # print("transaction fee", transaction.fee())
        print("트랜잭션 수수료가 0 보다 큰가요?", transaction.fee() > 0 )

    def exercise8(self):
        print("********** [ 서명 확인 ] **********")
        sec = bytes.fromhex('0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        der = bytes.fromhex('3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed')
        z = 0x27e0c5994dec7824e56dec6b2fcb342eb7cdb0d0957c2fce9882f715e85d81a6

        public_point = S256Point.parse(sec)
        signature = Signature.parse(der)
        print('서명이 유효한가요?', public_point.verify(z, signature))

    def exercise9(self):
        """
        서명 해시 z 값 구하기 로직
        1. 해제스크립트 부분 대신에 잠금스크립트로 대체한다.
        2. 1의 결과 값을 hash256 작업을 수행한다.
        3. 2의 결과 값을 32byte 빅엔디언 정수형으로 변환.    # 서명해시 값 생성
        """
        print("********** [ 서명 해시 z 값 구하기 ] **********")
        ## 서명해시 값을 이전 트랜잭션의 잠금 스크립트로 대체한 값
        modified_transaction = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000001976a914a802fc56c704ce87c42d7c92eb75e7896bdc41ae88acfeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943060001000000')
        hash256_value = hash256(modified_transaction)
        z = int.from_bytes(hash256_value, 'big')        # 서명해시 값
        print("서명해시 값:", hex(z))

    def exercise10(self):
        print("********** [ 서명 검증하기 ] **********")
        sec = bytes.fromhex('0349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278a')
        der = bytes.fromhex('3045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed')

        ## 공개키, 서명 값 구하기
        public_key = S256Point.parse(sec)   # 역질렬화 -> 공개키 나옴
        signature = Signature.parse(der)    # 역질렬화 -> 서명 나옴

        ## 서명 해시 z 값 구하기
        modified_transaction = bytes.fromhex('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000001976a914a802fc56c704ce87c42d7c92eb75e7896bdc41ae88acfeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac1943060001000000')
        hash256_value = hash256(modified_transaction)
        z = int.from_bytes(hash256_value, 'big')

        ## 검증  수행
        print("검증 결과:", public_key.verify(z, signature))


    def exercise11(self):
        print("********** [ 트랜잭션 생성하기 ] **********")
        # from helper import decode_base58, SIGHASH_ALL
        # from script import p2pkh_script, Script
        # from tx import TxIn, TxOut, Tx
        SATOSHI = 100000000

        previous_transaction = bytes.fromhex('0d6fe5213c0b3291f208cba8bfb59b7476dffacc4e5cb66f6eb20a080843a299')
        previous_index = 13

        transaction_inputs= TransactionIn(previous_transaction=previous_transaction, previous_index=previous_index)

        transaction_oupts = []

        change_amount = int(0.33 * SATOSHI)                                     # 사토시 단위, 1비트당 1억 사토시
        change_h160 = decode_base58('mzx5YhAH9kNHtcN481u6WkjeHjYtVeKVh2')
        change_script = p2pkh_script(change_h160)
        change_output = TransactionOut(amount=change_amount, script_public_key=change_script)

        target_amount = int(0.1 * SATOSHI)                                      # 사토시 단위, 1비트당 1억 사토시
        target_h160 = decode_base58('mnrVtF8DWjMu839VW3rBfgYaAfKk8983Xf')
        target_script = p2pkh_script(target_h160)
        target_output = TransactionOut(amount=target_amount, script_public_key=target_script)

        tx_obj = Transaction(1, [transaction_inputs], [change_output, target_output], 0, True)  # 테스트 넷
        # transation_object = Transaction(1, )
        print('tx_obj', tx_obj)

    def exercise12(self):

        ## 트랜잭션 얻기
        # tx = TxFetcher2.fetch('1dcdfdbcdd3ccb8bceb7a984386454a9df6ea841a251017938d3691cfb006318', testnet=True)
        secret = little_endian_to_int(b'gyu secret')
        z = int.from_bytes(hash256(b"gyu's message"), 'big') # 메시지 생성

        private_key = PrivateKey(secret)
        private_key_secret = private_key.secret
        public_key = private_key.point

        print('비밀키', private_key_secret)
        print('공개키', public_key)
        print('메시지', z)

        sign = private_key.sign(z)
        print('서명', sign)
        print()


        # sec = public_key.sec().hex()
        # der = sign.der().hex()
        # print('공개키 직렬화', sec)
        # print('서명 직렬화', der)

        print('서명 검증:', public_key.verify(z, sign))



        # print('point', private_key.point.sec().hex())
        # address = private_key.point.address()       # 비트코인 주소
        # public_key = decode_base58(address)




        ##### 12 문제
        # raw_tx = ('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        # stream = BytesIO(bytes.fromhex(raw_tx))
        # transaction = Transaction.parse(stream)
        # print("transaction", transaction)
        #
        # print("********** [ 해제 스크립트 생성하기 ] **********")     # 위에서 생성한 트랜잭션의 해제 스크립트
        # index = 0
        #
        # z = transaction.signature_hash(index)
        # private_key = PrivateKey(secret=8675309)
        # der = private_key.sign(z).der()                 # 메시지 서명 생성 후 직렬화
        # signature = der + SIGNATURE_HASH_ALL.to_bytes(1, 'big')     # 스크립트에 들어가는 서명은 DER 형식 + 1byte 해시 유형
        # sec = private_key.point.sec()
        # script_signature = Script([signature, sec])
        # transaction.tx_inputs[index].script_signature = script_signature
        # transaction.verify()
        # # print(transaction.serialize().hex())

    def exercise13(self):
        print("********** [ 비트코인 주소 생성 ] **********")
        secret = little_endian_to_int(b'gyu secret')
        print('secret', secret)
        private_key = PrivateKey(secret)
        print("private_key.secret", private_key.secret)
        public_point = private_key.point.address(compressed=True, testnet=True)
        print("public_point", public_point)         # mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx

    def exercise14(self):
        print("********** [  ] **********")
        SATOSHI = 100000000

        ## 이전트랜잭션에서 나의 정보?
        previous_transaction = bytes.fromhex('1dcdfdbcdd3ccb8bceb7a984386454a9df6ea841a251017938d3691cfb006318')
        previous_index = 0

        ## 목적지
        target_address = 'mtSYsqiRFrfaTAN7y1EvBb3CBEadEF1a9R'       # 목적지 지갑 주소
        target_amount = 0.00001

        change_address = 'mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx'       # 자기 주소로 반환
        change_amount = 0.00008


        secret = little_endian_to_int(b'gyu secret')

        private_key = PrivateKey(secret=secret)
        tx_inputs = []
        tx_inputs.append(TransactionIn(previous_transaction, previous_index))
        print('tx_inputs', tx_inputs)


        ## 목적 출력 생성
        tx_outputs = []
        target_hash160_value = decode_base58(target_address)               # 목적지 hash160 값
        script_public_key = p2pkh_script(target_hash160_value)             # 잠금 스크립트
        target_satoshis = int(target_amount * SATOSHI)
        tx_outputs.append(TransactionOut(target_satoshis, script_public_key))
        # print('target_satoshis', target_satoshis)

        ## 잔돈을 받는 (자신에게 보내는) 출력 생성
        change_hash160_value = decode_base58(change_address)
        script_public_key = p2pkh_script(change_hash160_value)
        change_satoshis = int(change_amount * SATOSHI)
        # print("change_satoshis", change_satoshis)

        tx_outputs.append(TransactionOut(change_satoshis, script_public_key))

        transaction_object = Transaction(1, tx_inputs, tx_outputs, 0, testnet=True)
        # print('tx_se', transaction_object.serialize().hex())
        raw_tx = transaction_object.serialize().hex()

        stream = BytesIO(bytes.fromhex(raw_tx))
        transaction = Transaction.parse(stream)
        print("transaction", transaction)

        print("********** [ 해제 스크립트 생성하기 ] **********")     # 위에서 생성한 트랜잭션의 해제 스크립트
        index = 0

        z = transaction.signature_hash(index)
        private_key = PrivateKey(secret=8675309)
        der = private_key.sign(z).der()                 # 메시지 서명 생성 후 직렬화
        signature = der + SIGNATURE_HASH_ALL.to_bytes(1, 'big')     # 스크립트에 들어가는 서명은 DER 형식 + 1byte 해시 유형
        sec = private_key.point.sec()
        script_signature = Script([signature, sec])
        transaction.tx_inputs[index].script_signature = script_signature
        transaction.verify()
        # print(transaction.serialize().hex())

        """
        raw_tx = ('0100000001813f79011acb80925dfe69b3def355fe914bd1d96a3f5f71bf8303c6a989c7d1000000006b483045022100ed81ff192e75a3fd2304004dcadb746fa5e24c5031ccfcf21320b0277457c98f02207a986d955c6e0cb35d446a89d3f56100f4d7f67801c31967743a9c8e10615bed01210349fc4e631e3624a545de3f89f5d8684c7b8138bd94bdd531d2e213bf016b278afeffffff02a135ef01000000001976a914bc3b654dca7e56b04dca18f2566cdaf02e8d9ada88ac99c39800000000001976a9141c4bc762dd5423e332166702cb75f40df79fea1288ac19430600')
        stream = BytesIO(bytes.fromhex(raw_tx))
        transaction = Transaction.parse(stream)
        print("transaction", transaction)

        print("********** [ 해제 스크립트 생성하기 ] **********")     # 위에서 생성한 트랜잭션의 해제 스크립트
        index = 0

        z = transaction.signature_hash(index)
        private_key = PrivateKey(secret=8675309)
        der = private_key.sign(z).der()                 # 메시지 서명 생성 후 직렬화
        signature = der + SIGNATURE_HASH_ALL.to_bytes(1, 'big')     # 스크립트에 들어가는 서명은 DER 형식 + 1byte 해시 유형
        sec = private_key.point.sec()
        script_signature = Script([signature, sec])
        transaction.tx_inputs[index].script_signature = script_signature
        print(transaction.serialize().hex())
        """

        # print('tx_output', tx_outputs)
        # sec = private_key.point.sec()
        # print('sec', sec.hex())
        # private_key.sign()
        # print('target', decode_base58(target_address).hex())
        # print('change', decode_base58(change_address).hex())

        # transaction_object = Transaction(1, tx_inputs, tx_outputs, 0, testnet=True)
        # print(transaction_object.signature_input(0, private_key))
        # print('** transaction_object ** ', transaction_object)
        # print('** transaction_object fee ** ', transaction_object.fee())
        # print('트랜잭션 검증:', transaction_object.verify())

        # print('트랜잭션 직렬화:', transaction_object.serialize().hex())


        # change_hash160_value = decode_base58(change_address)
        # scri




## 테스트 코드 실행
# run(TransactionTest("test_parse_version"))      # 트랜잭션 버전 parse 테스트
# run(TransactionTest("test_parse_inputs"))       # 트랜잭션 inputs parse 테스트
# run(TransactionTest("test_parse_outputs"))      # 트랜잭션 outputs parse 테스트
# run(TransactionTest("test_parse_locktime"))     # 트랜잭션 lokctime parse 테스트

# run(TransactionTest("test_serialize"))          #
# run(TransactionTest("test_input_value"))        #
# run(TransactionTest("test_input_pubkey"))       #



# run(TransactionTest("test_fee"))                # 트랜잭션 수수료 테스트

# run(TransactionTest("test_sig_hash"))           #
# run(TransactionTest("test_sig_hash2"))          #

# run(TransactionTest("test_verify_p2pkh"))       #
# run(TransactionTest("test_verify_p2pkh2"))      #

# run(TransactionTest("test_verify_p2sh"))        #
# run(TransactionTest("test_verify_p2sh2"))       #

# run(TransactionTest("test_sign_input"))         #


## 책 예제 테스트 코드 실행
# run(TransactionTest("exercise1"))               # 트랜잭션 값, 버전만 parsing 하기
# run(TransactionTest("exercise2"))               # byte 값을 정수로 변환하는 예제
# run(TransactionTest("exercise3"))               # 스크립트 파싱
# run(TransactionTest("exercise4"))               # 트랜잭션 필드 값 찾기
# run(TransactionTest("exercise5"))               # 실제 트랜잭션 값 파싱 및 수수료 파싱하기
# run(TransactionTest("exercise6"))               # 트랜잭션 필드 값 찾기
# run(TransactionTest("exercise7"))               # 트랜잭션 수수료 검증
# run(TransactionTest("exercise8"))               # 서명 검증
# run(TransactionTest("exercise9"))               # 서명 해시 z 값 구하기
# run(TransactionTest("exercise10"))              # 서명 검증하기
# run(TransactionTest("exercise11"))              # 서명 생성하기
run(TransactionTest("exercise12"))              #
# run(TransactionTest("exercise13"))              # 비트코인 주소 생성


# run(TransactionTest("exercise14"))              #
