# import os
# import sys
# sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))

import os
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
path = os.path.split(path)[0]                                       # 상위 디렉토리 추출

import sys
sys.path.append(path)                                               # path 지정

import requests

from lib.helper import (run, little_endian_to_int, hash256, decode_base58, SIGNATURE_HASH_ALL)
from src.transaction import Transaction
from src.transactionIn import TransactionIn
from src.transactionOut import TransactionOut
from src.script import (Script, p2pkh_script)
from src.s256Point import S256Point
from src.signature import Signature
from src.privatekey import PrivateKey
# from src.transactionFetcher import TxFetcher
from src.api import TxFetcher
from lib.config import FETCH_HEADERS_OPTION


##################################################### sochain api 사용
SATOSHI = 100000000

##
# from_address = 'mtSYsqiRFrfaTAN7y1EvBb3CBEadEF1a9R'
# secret = 70873993407854360621546794063556470285548175334479602829309254556818321296529
# mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx

## 필요한 정보
fee = 0.00001 * SATOSHI
from_address = 'mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx'
secret = 549665875707611667855719
target_amount = 0.01 *SATOSHI
to_address = 'mtSYsqiRFrfaTAN7y1EvBb3CBEadEF1a9R'


#
# def utxoFetch(from_address):
#     transactions = TxFetcher.fetchUTXO(from_address, testnet=True)
#     return transactions


def get_total_money(from_address):
    url = 'http://ingyu.kr:18334/utxo/'+from_address
    response = requests.get(url)
    datas = response.json()
    total_money = 0
    # 에러 처리 UTXO 가 없을 경우
    if len(datas) == 0:
        return total_money

    ## UTXO 가 있기에 토탈 잔액 구하기

    for data in datas:
        total_money += data['value']

    # print('총합', total_money)

    return total_money



##### block-cypher api
# def get_total_money(from_address):
#     SATOSHI = 100000000
#     print('address', from_address)
#
#     transactions = TxFetcher.fetchUTXO(from_address, testnet=True)
#     total_money = 0
#     for transaction in transactions:
#         total_money += transaction['value']
#     total_money /= SATOSHI
#
#     return total_money

def getUTXO3():
    print("UTXO 가져온 후 돈 보낼양을 알아서 계산후 트랜잭션 생성 및 sendTransaction 호출하기")

    private_key = PrivateKey(secret=secret)


    tx_inputs = []
    tx_outputs = []

    ## UTXO 가져오기
    transactions = TxFetcher.fetchUTXO(from_address, testnet=True)

    total_money = 0
    for index, tx in enumerate(transactions):
        transaction = transactions[index]

        # 트랜잭션 만들기
        prev_tx = bytes.fromhex(transaction['transaction_id'])      # UTXO 거래 id
        prev_index = transaction['output_number']                   # UTXO 인덱스
        from_value = float(transaction['value'])                    # 내가 갖고  있는 금액
        print('from_value', from_value)
        total_money += from_value
        tx_inputs.append(TransactionIn(prev_tx, prev_index))

        if total_money > target_amount:
            break


    print('total_money:', total_money)
    print('target-amount:', target_amount)
    print('fee', fee)

    # target_amount = target_amount * SATOSHI
    # fee =

    change_amount = total_money - (target_amount + fee)

    print('change_amount:', change_amount)
    if change_amount <= 0:
        print("수수료 오류")
        return False

    h160 = decode_base58(to_address)
    script_pubkey = p2pkh_script(h160)
    target_satoshis = int(target_amount)
    tx_outputs.append(TransactionOut(target_satoshis, script_pubkey))

    h160 = decode_base58(from_address)
    script_pubkey = p2pkh_script(h160)
    change_satoshis = int(change_amount)
    tx_outputs.append(TransactionOut(change_satoshis, script_pubkey))

    tx_obj = Transaction(1, tx_inputs, tx_outputs, 0, testnet=True)
    for index in range(len(tx_inputs)):
        print(f'해제스크립트 서명 검증{index}: ', tx_obj.signature_input(index, private_key))


    print('tx_obj', tx_obj.serialize().hex())
    # # ## 트랜잭션 보내기
    url = 'https://sochain.com/api/v2/send_tx/BTCTEST'
    data = {
        'tx_hex' : tx_obj.serialize().hex()
    }

    response = requests.post(url, data=data, headers=FETCH_HEADERS_OPTION)
    print('response:', response)
    print('response json:', response.json())

# getUTXO3()



############
# def getUTXO2():
#     print("UTXO 가져온 후 돈 보낼양을 알아서 계산후 트랜잭션 생성")
#
#     private_key = PrivateKey(secret=secret)
#
#
#     tx_inputs = []
#     tx_outputs = []
#
#     ## UTXO 가져오기
#     transactions = TxFetcher.fetchUTXO(from_address, testnet=True)
#
#
#     total_money = 0
#     for index, tx in enumerate(transactions):
#         print(index, tx)
#         transaction = transactions[index]
#
#         # 트랜잭션 만들기
#         prev_tx = bytes.fromhex(transaction['transaction_id'])      # UTXO 거래 id
#         prev_index = transaction['output_number']                   # UTXO 인덱스
#         from_value = float(transaction['value'])                    # 내가 갖고  있는 금액
#
#         total_money += from_value
#         tx_inputs.append(TransactionIn(prev_tx, prev_index))
#
#         if total_money > target_amount:
#             break
#
#
#     print('total_money:', total_money)
#
#     change_amount = total_money - (target_amount + fee)
#
#
#     if change_amount <= 0:
#         print("수수료 오류")
#         return False
#
#     h160 = decode_base58(to_address)
#     script_pubkey = p2pkh_script(h160)
#     target_satoshis = int(target_amount * SATOSHI)
#     tx_outputs.append(TransactionOut(target_satoshis, script_pubkey))
#
#     h160 = decode_base58(from_address)
#     script_pubkey = p2pkh_script(h160)
#     change_satoshis = int(change_amount * SATOSHI)
#     tx_outputs.append(TransactionOut(change_satoshis, script_pubkey))
#
#
#     tx_obj = Transaction(1, tx_inputs, tx_outputs, 0, testnet=True)
#     for index in range(len(tx_inputs)):
#         if not tx_obj.signature_input(index, private_key):
#             print("해제스크립트 서명 검증 실패")
#             return False
#
#     print(tx_obj.serialize().hex())
#
# getUTXO2()


##################
# def getUTXO():
#     print("UTXO 값 가져온 후 하나의 인풋으로 처리하기")
#     # from_address = 'mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx'
#
#     ## UTXO 가져오기
#     transactions = TxFetcher.fetchUTXO(from_address, testnet=True)
#
#     transaction = transactions[0]
#     tx_inputs = []
#     tx_outputs = []
#
#
#     # 트랜잭션 만들기
#     prev_tx = bytes.fromhex(transaction['transaction_id'])
#     prev_index = transaction['output_number']
#     from_value = int(transaction['value'])
#
#     print('from_value', from_value)
#
#
#     ## 잔돈 구하기 - 거스름돈
#     change_amount = from_value - (target_amount + fee)
#
#     print('fee', fee)
#     print('target_amount', target_amount)
#     print('change_amount', change_amount)
#
#     if change_amount <= 0:
#         print("수수료 오류")
#         return False
#
#     private_key = PrivateKey(secret=secret)
#     tx_inputs.append(TransactionIn(prev_tx, prev_index))
#
#     ## output
#     h160 = decode_base58(to_address)
#     script_pubkey = p2pkh_script(h160)
#     target_satoshis = int(target_amount)
#     tx_outputs.append(TransactionOut(target_satoshis, script_pubkey))
#
#     h160 = decode_base58(from_address)
#     script_pubkey = p2pkh_script(h160)
#     change_satoshis = int(change_amount)
#     tx_outputs.append(TransactionOut(change_satoshis, script_pubkey))
#
#     tx_obj = Transaction(1, tx_inputs, tx_outputs, 0, testnet=True)
#     print('해제스크립트 서명 검증: ', tx_obj.signature_input(0, private_key))
#     if not tx_obj.signature_input(0, private_key):
#         return False
#
#     print(tx_obj.serialize().hex())
#
# getUTXO()


##########
# def from_inputs_to_output():
#     print('[여러개의 인풋에서 하나의 아웃풋 생성]') # - 잔돈은 나한테 보냄
#     prev_tx_1 = bytes.fromhex('69e6fcc57490c93e1fd9afbd92804546e49124e47485f2b99a41e2d6c3ad26e7')   # 0.01603999
#     prev_index_1 = 1
#     prev_tx_2 = bytes.fromhex('720a99e27e6f1f414407668192c444e54e3b64d3382037a6a33c6ab222ca72a0')   # 0.02160000
#     prev_index_2 = 1
#     target_address = 'mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx'
#     target_amount = 0.037
#     secret = 70873993407854360621546794063556470285548175334479602829309254556818321296529
#     priv = PrivateKey(secret=secret)
#
#     ##
#     tx_ins = []
#     tx_ins.append(TransactionIn(prev_tx_1, prev_index_1))
#     tx_ins.append(TransactionIn(prev_tx_2, prev_index_2))
#
#     ##
#     tx_outs = []
#     h160 = decode_base58(target_address)
#     script_pubkey = p2pkh_script(h160)
#     target_satoshis = int(target_amount * SATOSHI)
#     tx_outs.append(TransactionOut(target_satoshis, script_pubkey))
#
#
#     tx_obj = Transaction(1, tx_ins, tx_outs, 0, testnet=True)
#
#     print('', tx_obj.signature_input(0, priv))
#     print('', tx_obj.signature_input(1, priv))
#     print(tx_obj.serialize().hex())
# from_inputs_to_output()


