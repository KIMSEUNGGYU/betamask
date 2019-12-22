import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
import requests
from io import BytesIO
import json

from lib.helper import little_endian_to_int

BASE_URL = 'https://sochain.com/api/v2/get_tx/'
MAIN_NET = 'BTC/'
TEST_NET = 'BTCTEST/'

class TxFetcher:
    cache = {}

    @classmethod
    def fetch(cls, transaction_id, testnet=False):
        cls.load_cache('./tx')

        headers_option = {
            'Host': 'sochain.com',
            # 'Connection': 'keep-alive',
            # 'Pragma': 'no-cache',
            # 'Cache-Control': 'no-cache',
            # 'DNT': '1',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            # 'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9;*',
            # 'Sec-Fetch-Site': 'same-origin',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Referer': 'https://sochain.com/api/v2/get_tx/BTCTEST/1dcdfdbcdd3ccb8bceb7a984386454a9df6ea841a251017938d3691cfb006318',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': '__cfduid=df75ba7d6a3580c36abf35b749197ad351576993478; _ga=GA1.2.552005313.1576993773; cf_clearance=cde33a8e14fccb7be83333e850b174ac16d25012-1576999325-0-150'
        }

        if transaction_id not in cls.cache:
            if testnet:
                url = BASE_URL + TEST_NET
            else:
                url = BASE_URL + MAIN_NET
            url += transaction_id

            response = requests.get(url, headers=headers_option)
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


