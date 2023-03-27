#!/usr/bin/env python
# coding: utf-8

# In[26]:


from web3 import Web3
from solcx import install_solc
from solcx import compile_source
import solcx

install_solc(version='latest')

onchain = Web3(Web3.HTTPProvider('http://192.168.1.49:8545')) #on-chain

s1 = Web3(Web3.HTTPProvider('http://192.168.1.49:8546')) #shard 1
s2 = Web3(Web3.HTTPProvider('http://192.168.1.49:8547')) #shard 2
s3 = Web3(Web3.HTTPProvider('http://192.168.1.49:8548')) #shard 3

onchain.isConnected(), s1.isConnected(), s2.isConnected(), s3.isConnected()


# In[12]:


compiled_sol = compile_source(
     '''
     pragma solidity >0.5.0;

     contract Greeter {
         string public greeting;

         constructor() public {
             greeting = 'Hello';
         }

         function setGreeting(string memory _greeting) public {
             greeting = _greeting;
         }

         function greet() view public returns (string memory) {
             return greeting;
         }
     }
     ''',
     output_values=['abi', 'bin']
)


# In[13]:


contract_id, contract_interface = compiled_sol.popitem()

bytecode = contract_interface['bin']
abi = contract_interface['abi']


# In[16]:


s1.eth.default_account = w3.eth.accounts[0]
Greeter = s1.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Greeter.constructor().transact()
tx_receipt = s1.eth.wait_for_transaction_receipt(tx_hash)


# In[21]:


greeter = s1.eth.contract(
     address=tx_receipt.contractAddress,
     abi=abi
)


# In[23]:


greeter.functions.greet().call()


# In[25]:


tx_hash = greeter.functions.setGreeting('Ue bellezz').transact()

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
greeter.functions.greet().call()


# In[ ]:




