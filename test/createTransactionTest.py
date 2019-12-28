import os
import sys
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
sys.path.append(os.path.abspath(path))

import requests
from io import BytesIO

from lib.helper import (run, little_endian_to_int, hash256, decode_base58, SIGNATURE_HASH_ALL)
from src.transaction import Transaction
from src.transactionIn import TransactionIn
from src.transactionOut import TransactionOut
from src.script import (Script, p2pkh_script)
from src.s256Point import S256Point
from src.signature import Signature
from src.privatekey import PrivateKey
from src.transactionFetcher import TxFetcher

SATOSHI = 100000000


def inputs_one_output():
    print('[여러개의 인풋에서 하나의 아웃풋 생성]') # - 잔돈은 나한테 보냄
    prev_tx_1 = bytes.fromhex('69e6fcc57490c93e1fd9afbd92804546e49124e47485f2b99a41e2d6c3ad26e7')   # 0.01603999
    prev_index_1 = 1
    prev_tx_2 = bytes.fromhex('720a99e27e6f1f414407668192c444e54e3b64d3382037a6a33c6ab222ca72a0')   # 0.02160000
    prev_index_2 = 1
    target_address = 'mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx'
    target_amount = 0.037
    secret = 70873993407854360621546794063556470285548175334479602829309254556818321296529
    priv = PrivateKey(secret=secret)

    ##
    tx_ins = []
    tx_ins.append(TransactionIn(prev_tx_1, prev_index_1))
    tx_ins.append(TransactionIn(prev_tx_2, prev_index_2))

    ##
    tx_outs = []
    h160 = decode_base58(target_address)
    script_pubkey = p2pkh_script(h160)
    target_satoshis = int(target_amount * SATOSHI)
    tx_outs.append(TransactionOut(target_satoshis, script_pubkey))

    tx_obj = Transaction(1, tx_ins, tx_outs, 0, testnet=True)
    print('', tx_obj.signature_input(0, priv))
    print('', tx_obj.signature_input(1, priv))
    print(tx_obj.serialize().hex())



inputs_one_output()

def one_input_ouputs():
    print('[하나의 인풋에서 두개의 아웃풋 생성]') # - 잔돈은 나한테 보냄
    prev_tx = bytes.fromhex('bfb2fc892fe2a14335d392fe894e92f0788476ad82722e545a3eb2f7167a2063')
    prev_index = 1

    target_address = 'mq4zcoFEimt2vmYutHZ3jC9gLE9sehejRx'
    target_amount = 0.01

    change_address = 'mtSYsqiRFrfaTAN7y1EvBb3CBEadEF1a9R'
    change_amount = 0.01604

    secret = 70873993407854360621546794063556470285548175334479602829309254556818321296529
    priv = PrivateKey(secret=secret)

    tx_ins = []
    tx_ins.append(TransactionIn(prev_tx, prev_index))

    tx_outs = []
    h160 = decode_base58(target_address)
    script_pubkey = p2pkh_script(h160)
    target_satoshis = int(target_amount*100000000)
    tx_outs.append(TransactionOut(target_satoshis, script_pubkey))

    h160 = decode_base58(change_address)
    script_pubkey = p2pkh_script(h160)
    change_satoshis = int(change_amount*100000000)
    tx_outs.append(TransactionOut(change_satoshis, script_pubkey))

    tx_obj = Transaction(1, tx_ins, tx_outs, 0, testnet=True)
    print(tx_obj.signature_input(0, priv))
    print(tx_obj.serialize().hex())


# one_input_ouputs()