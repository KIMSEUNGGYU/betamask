# import os
# import sys
# sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
import requests
from io import BytesIO
import json

from lib.helper import little_endian_to_int
from lib.config import FETCH_HEADERS_OPTION

class Fetcher:
    tx_cache = []

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


    @classmethod
    def fetchUTXO(cls, bitcoin_address, testnet=True):
        url = 'http://ingyu.kr:18334/utxo/'+bitcoin_address
        response = requests.get(url)
        datas = response.json()
        # total_money = 0
        # 에러 처리 UTXO 가 없을 경우

        # UTXO 가 없음
        if len(datas) == 0:
            return False

        ## UTXO 가 있기에 토탈 잔액 구하기

        for data in datas:
            print('data', data)
            # total_money += data['value']

        # BASE_URL = 'https://sochain.com/api/v2/get_tx_unspent/'
        # if bitcoin_address not in cls.cache:
        #     if testnet:
        #         url = BASE_URL + TEST_NET
        #     else:
        #         url = BASE_URL + MAIN_NET
        #     url += bitcoin_address
        #
        #     print('url', url)
        #
        #     ## 프로그램 설정 데이터
        #     response = requests.get(url, headers=FETCH_HEADERS_OPTION)
        #     if response.status_code == 200:
        #         transactions = []
        #
        #         try:
        #             raw_txs = response.json()['data']['txs']
        #         except ValueError:
        #             raise ValueError(f'unexpected response: {response.json()}')
        #
        #         for raw_tx in raw_txs:
        #             txid = raw_tx['txid']
        #             output_number = raw_tx['output_no']
        #             value = raw_tx['value']
        #
        #             transaction = {
        #                 'transaction_id':txid,
        #                 'output_number': output_number,
        #                 'value': value
        #             }
        #             transactions.append(transaction)
        #
        #
        #         cls.cache[bitcoin_address] = transactions
        #         cls.utxo_dump_cache('utxo')
        #
        #         return transactions
        #     else:
        #         print('[ERROR] NO RESPONSE ,  ', response)
        # else:
        #     return cls.cache[bitcoin_address]


    @classmethod
    def fetch(cls, transaction_id, testnet=False):
        url = 'http://ingyu.kr:18334/tx/' + transaction_id

        response = requests.get(url)
        print('response', response.json()['hex'])
        from src.transaction import Transaction
        try:
            # raw = response.json()['data']['hex']
            raw = response.json()['hex']
        except ValueError:
            raise ValueError(f'unexpected response: {response.json()}')

        raw = bytes.fromhex(raw.strip())
        if raw[4] == 0:
            raw = raw[:4] + raw[6:]
            tx = Transaction.parse(BytesIO(raw.strip()), testnet=testnet)
            tx.locktime = little_endian_to_int(raw[-4:])
        else:
            try:
                tx = Transaction.parse(BytesIO(raw.strip()), testnet=testnet)
            except:
                print("error")

        if tx.id() != transaction_id:
            raise ValueError(f'not the same id: {tx.id()} vs {transaction_id}')

        return tx
