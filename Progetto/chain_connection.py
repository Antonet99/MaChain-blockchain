from web3 import Web3
from solcx import install_solc, compile_standard
import solcx
import json


class EthereumConnection:
    def __init__(self, url):
        self.url = url
        self.web3 = Web3(Web3.HTTPProvider(self.url))

    def is_connected(self):
        return self.web3.is_connected()


onchain = EthereumConnection('http://192.168.1.100:8545')
s1 = EthereumConnection('http://192.168.1.100:8546')
s2 = EthereumConnection('http://192.168.1.100:8547')
s3 = EthereumConnection('http://192.168.1.100:8548')

print(onchain.is_connected(), s1.is_connected(),
      s2.is_connected(), s3.is_connected())
