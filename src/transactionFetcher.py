import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
import requests
from io import BytesIO
import json

from lib.helper import little_endian_to_int
from lib.config import FETCH_HEADERS_OPTION

BASE_URL = 'https://sochain.com/api/v2/get_tx/'
MAIN_NET = 'BTC/'
TEST_NET = 'BTCTEST/'

class TxFetcher:
    cache = {}

    @classmethod
    def fetch(cls, transaction_id, testnet=False):
        cls.load_cache('./tx')

        if transaction_id not in cls.cache:
            if testnet:
                url = BASE_URL + TEST_NET
            else:
                url = BASE_URL + MAIN_NET
            url += transaction_id

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

                cls.cache[transaction_id] = tx
                cls.cache[transaction_id].testnet = testnet
                cls.dump_cache('tx')
                return cls.cache[transaction_id]
            else:
                print('[ERROR] NO RESPONSE ,  ', response)
        else:
            return cls.cache[transaction_id]

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
            cls.cache[k] = tx

    @classmethod
    def dump_cache(cls, filename):
        with open(filename, 'w') as f:
            to_dump = {k: tx.serialize().hex() for k, tx in cls.cache.items()}
            s = json.dumps(to_dump, sort_keys=True, indent=4)
            f.write(s)


