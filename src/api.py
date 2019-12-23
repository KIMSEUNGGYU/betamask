import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
import requests
from io import BytesIO
from lib.helper import (little_endian_to_int)

class TxFetcher():
    @classmethod
    def fetch(cls, tx_id, testnet):
        base_url = 'https://api.blockcypher.com/v1/btc/test3/'
        method = 'txs/'
        option = '?includeHex=true'
        url = base_url + method + tx_id + option

        response = requests.get(url)
        if response.status_code == 200:
            from src.transaction import Transaction
            data = response.json()
            # print('data', data['hex'])
            # tx_hex = data['hex']
            # return tx_hex

            raw = data['hex']
            raw = bytes.fromhex(raw.strip())
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Transaction.parse(BytesIO(raw.strip()), testnet=True)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                try:
                    tx = Transaction.parse(BytesIO(raw.strip()), testnet=True)
                except:
                    print("error")

            if tx.id() != tx_id:
                raise ValueError(f'not the same id: {tx.id()} vs {tx_id}')


            return tx
            # cls.cache[transaction_id] = tx
            # cls.cache[transaction_id].testnet = testnet
            # # cls.dump_cache('tx')
            # return cls.cache[transaction_id]
        else:
            print("비정상 상태")

    @classmethod
    def fetchUTXO(cls, address, testnet=True):
        # print('api, fetch')
        base_url = 'https://api.blockcypher.com/v1/btc/test3/'
        method = 'addrs/'

        ## false 가 안보낸거 - UTXO 사용 안한거
        url = base_url + method + address
        # print('url:', url)
        response = requests.get(url, {
            'unspentOnly': True,
        })


        utxo_transaction = []
        if response.status_code == 200:
            print("정상적 수행")
            datas = response.json()
            txrefs = datas['txrefs']

            # 트랜잭션 중에서 UTXO 가능한 것들 추출
            for tx in txrefs:
                if 'spent' in tx.keys():
                    if tx['spent'] == False:
                        raw_tx = {
                            'transaction_id': tx['tx_hash'],
                            'output_number': tx['tx_output_n'],
                            'value': tx['value']
                        }
                        utxo_transaction.append(raw_tx)
        else:
            print("비정상 상태")

        # print('utxo:', utxo_transaction[0])
        # print('UTXO 트랜잭션 가능 갯수:', len(utxo_transaction))
        # print('UTXO 트랜잭션 모음: ',utxo_transaction)
        return utxo_transaction
