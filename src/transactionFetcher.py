import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
import requests
from io import BytesIO
import json

from lib.helper import little_endian_to_int
from lib.config import FETCH_HEADERS_OPTION

MAIN_NET = 'BTC/'
TEST_NET = 'BTCTEST/'

class TxFetcher:
    cache = {}
    tx_cache = {}

    @classmethod
    def fetchUTXO(cls, bitcoin_address, testnet=True):
        cls.utxo_load_cache('./utxo')

        BASE_URL = 'https://sochain.com/api/v2/get_tx_unspent/'
        if bitcoin_address not in cls.cache:
            if testnet:
                url = BASE_URL + TEST_NET
            else:
                url = BASE_URL + MAIN_NET
            url += bitcoin_address

            print('url', url)

            ## 프로그램 설정 데이터
            FETCH_HEADERS_OPTION = {
                'Host': 'sochain.com',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9;*',
                'Cookie': 'cf_clearance=04d471ba1c07724e4a2dac4f25fada48baecc4b6-1577100896-0-150;'
            }
            response = requests.get(url, headers=FETCH_HEADERS_OPTION)
            if response.status_code == 200:
                transactions = []

                try:
                    raw_txs = response.json()['data']['txs']
                except ValueError:
                    raise ValueError(f'unexpected response: {response.json()}')

                for raw_tx in raw_txs:
                    txid = raw_tx['txid']
                    output_number = raw_tx['output_no']
                    value = raw_tx['value']

                    transaction = {
                        'transaction_id':txid,
                        'output_number': output_number,
                        'value': value
                    }
                    transactions.append(transaction)


                cls.cache[bitcoin_address] = transactions
                cls.utxo_dump_cache('utxo')

                return transactions
            else:
                print('[ERROR] NO RESPONSE ,  ', response)
        else:
            return cls.cache[bitcoin_address]


    @classmethod
    def fetch(cls, transaction_id, testnet=False):
        # cls.load_cache('./tx')

        BASE_URL = 'https://sochain.com/api/v2/get_tx/'
        if transaction_id not in cls.tx_cache:
            if testnet:
                url = BASE_URL + TEST_NET
            else:
                url = BASE_URL + MAIN_NET
            url += transaction_id

            print('url', url)
            response = requests.get(url, headers=FETCH_HEADERS_OPTION)
            if response.status_code == 200:
                from src.transaction import Transaction
                # 응답 데이터 중에서 받고 싶은 데이터만 받기
                try:
                    raw = response.json()['data']['tx_hex']
                except ValueError:
                    raise ValueError(f'unexpected response: {response.json()}')

                # 받은 데이터를 transaction 객체로 만들기 위해 byte 로 변환
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

                cls.tx_cache[transaction_id] = tx
                cls.tx_cache[transaction_id].testnet = testnet
                cls.dump_cache('tx')
                return cls.tx_cache[transaction_id]
            else:
                print('[ERROR] NO RESPONSE ,  ', response)
        else:
            return cls.tx_cache[transaction_id]

    @classmethod
    def load_cache(cls, filename):

        from src.transaction import Transaction
        disk_cache = json.loads(open(filename, 'r').read())

        for k, raw_hex in disk_cache.items():
            raw = bytes.fromhex(raw_hex)
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Transaction.parse(BytesIO(raw))
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Transaction.parse(BytesIO(raw))
            cls.tx_cache[k] = tx

    @classmethod
    def dump_cache(cls, filename):
        with open(filename, 'w') as f:
            to_dump = {k: tx.serialize().hex() for k, tx in cls.tx_cache.items()}
            s = json.dumps(to_dump, sort_keys=True, indent=4)
            f.write(s)


    @classmethod
    def utxo_load_cache(cls, filename):
        disk_cache = json.loads(open(filename, 'r').read())

        for address, raw_txs in disk_cache.items():
            cls.cache[address] = raw_txs

    @classmethod
    def utxo_dump_cache(cls, filename):
        with open(filename, 'w') as f:
            to_dump = {k: tx for k, tx in cls.cache.items()}
            s = json.dumps(to_dump, sort_keys=True, indent=4)
            f.write(s)


