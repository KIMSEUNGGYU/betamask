import os
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
path = os.path.split(path)[0]                                       # 상위 디렉토리 추출
path = os.path.split(path)[0]                                       # 상위 디렉토리 추출

import sys
sys.path.append(os.path.abspath(path))

import blockcypher

from flask import jsonify
from flask import request
from models import Users, db
from tx_models import Tx_history, db2

from . import api  # __init__ 에 있는 api
from develop.bitcoin_api.mnemonic import (make_mnemonic, get_bitcoin_address)

from lib.helper import (run, little_endian_to_int, hash256, decode_base58, SIGNATURE_HASH_ALL)
from src.transaction import Transaction
from src.transactionIn import TransactionIn
from src.transactionOut import TransactionOut
from src.script import (Script, p2pkh_script)
from lib.config import FETCH_HEADERS_OPTION

from src.privatekey import PrivateKey
from lib.helper import (hash256, little_endian_to_int)
import requests
SATOSHI = 100000000



def get_secret(from_address):
    query_result = Users.query.filter(Users.address == from_address).first()

    ## 올바르지 않는 경우
    if query_result == None:
        return jsonify({'message': '잘못된 계정입니다.'}), 202       # 값은 수신했지만, 올바른 값 없음
    data = query_result.serialize
    password = data['password']
    password = password.encode()
    secret = hash256(password)
    secret = little_endian_to_int(secret)                               # 3. Private의 secret 은 정수이므로 바이트 값을 정수로 변환
    return secret


def get_outputs(to_address, to_amount, from_address, change_amount):
    tx_outputs = []

    h160 = decode_base58(to_address)
    script_pubkey = p2pkh_script(h160)
    target_satoshis = int(to_amount)
    tx_outputs.append(TransactionOut(target_satoshis, script_pubkey))

    h160 = decode_base58(from_address)
    script_pubkey = p2pkh_script(h160)
    change_satoshis = int(change_amount)
    tx_outputs.append(TransactionOut(change_satoshis, script_pubkey))

    return tx_outputs

def get_inputs(from_address, to_amount):
    tx_inputs = []

    url = 'http://ingyu.kr:18334/utxo/'+from_address
    response = requests.get(url)
    transactions = response.json()
    # print('datas', transactions)

    if len(transactions) == 0:
        return jsonify({'message': 'UTXO 가 존재하지 않습니다.'}), 202


    total_money = 0
    for index, tx in enumerate(transactions):
        transaction = transactions[index]

        # 트랜잭션 만들기
        prev_tx = bytes.fromhex(transaction['tx_hash'])      # UTXO 거래 id
        prev_index = transaction['tx_pos']                   # UTXO 인덱스
        from_value = float(transaction['value'])             # 내가 갖고  있는 금액

        total_money += from_value
        tx_inputs.append(TransactionIn(prev_tx, prev_index))

        if total_money > to_amount:
            break

    # print('tx_inputs', tx_inputs)
    return (tx_inputs, total_money)


@api.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        ## data 가져오기
        data = request.get_json()
        from_address = data['fromAddress']
        to_address = data['toAddress']
        to_amount = data['amount']


        fee = int(0.0001 * SATOSHI)
        to_amount = int(to_amount * SATOSHI)

        secret = get_secret(from_address)
        private_key = PrivateKey(secret=secret)                             # 4. Private 객체 생성 secret 과 공개키 생성

        tx_inputs, total_money = get_inputs(from_address, to_amount)

        change_amount = total_money - (to_amount + fee)
        if change_amount <= 0:
            print("수수료 오류")
            return jsonify({'message': '현재 잔액보다 보내는 돈이 더 많습니다.'}), 202

        tx_outputs = get_outputs(to_address, to_amount, from_address, change_amount)

        print('total_money', total_money)
        print('change_amount', change_amount)

        # print('tx_inputs', tx_inputs)
        # # 트랜잭션 생성
        tx_obj = Transaction(1, tx_inputs, tx_outputs, 0, testnet=True)
        # 해제 스크립트 서명 검증 및 트랜잭션 완벽히 구성
        for index in range(len(tx_inputs)):
            tx_obj.signature_input(index, private_key)


        # http://ingyu.kr:18334/tx/feebcbfd539873538bdb70b971ed3993c1030041f8ae2cc272154243de0a7774
        # print('tx_obj serialize', tx_obj.serialize().hex())
        #
        # print('ffff', blockcypher.get_total_balance('mtSYsqiRFrfaTAN7y1EvBb3CBEadEF1a9R', coin_symbol="btc-testnet"))

        ## 트랜잭션 보내기 - blockcypher
        try:
            transaction = blockcypher.pushtx(tx_hex=tx_obj.serialize().hex(), api_key="2ab5a455118a405290482d6232d4f051", coin_symbol="btc-testnet")
            transaction_hash = transaction['tx']['hash']
            # print('hex:', transaction_hash)

            tx_history = Tx_history()
            tx_history.address = from_address
            tx_history.tx = transaction_hash

            db2.session.add(tx_history)
            db2.session.commit()

            return jsonify({'message':transaction_hash}), 200
        except:
            return jsonify({'message': "트랜잭션 전송 오류"}), 202


        ## 트랜잭션 보내기 - sochain
        # url = 'https://sochain.com/api/v2/send_tx/BTCTEST'
        # data = {
        #     'tx_hex' : tx_obj.serialize().hex()
        # }

        # try:
        #     response = requests.post(url, data=data, headers=FETCH_HEADERS_OPTION)
        #     message = response.json()
        #     print('message', message)
        #     txid = message['data']['txid']
        #
        #     tx_history = Tx_history()
        #     tx_history.address = from_address
        #     tx_history.tx = txid
        #
        #     db2.session.add(tx_history)
        #     db2.session.commit()
        #
        #
        #
        #     return jsonify({'message':txid}), 200
        # except:
        #     return jsonify({'message': "트랜잭션 전송 오류"}), 202


@api.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')
        mnemonic = data.get('mnemonic')

        query_result = Users.query.filter(Users.mnemonic == mnemonic).first()

        ## 올바르지 않는 경우
        if query_result == None:
            return jsonify(), 202       # 값은 수신했지만, 올바른 값 없음

        data = query_result.serialize

        ## 올바른 경우 - 업데이트 진행

        print('data', data)

        data['fake_password'] = password

        print('data', data)
        Users.query.filter(Users.mnemonic == mnemonic).update(data)

        return jsonify(), 200
        # print('password', password)
        # print('mnemonic', mnemonic)

@api.route('/user/create', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')

        bitcoin_address = get_bitcoin_address(password)
        mnemonic_code = make_mnemonic(bitcoin_address)

        users = Users()
        users.address = bitcoin_address
        users.password = password
        users.fake_password = password
        users.mnemonic = mnemonic_code

        filter_result = Users.query.filter(Users.address == bitcoin_address).first()

        # 가입이 가능할 경우
        if filter_result == None:
            print("DB 에 저장")
            db.session.add(users)
            db.session.commit()
            return jsonify( {
                'address':bitcoin_address,
            }), 201

        ## 가입이 불가
        return jsonify(), 500
