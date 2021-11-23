
import datetime
import hashlib
import json
import time
from ellipticcurve import privateKey
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

# For creating accounts and signatures
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from werkzeug.wrappers import response


# creating a public and private key pair for the miner
miner_private_key = PrivateKey()
miner_public_key = miner_private_key.publicKey()


# This function is required for adding the number of zeros
def repeat(word, m, n):
    
    # if number of characters greater than length of word.
    # set number of characters = length of word
    if(m > len(word)):
        m = len(word)
          
    repeat_word = word[:m]
    result = ""
      
    for i in range(n):
        result = result+repeat_word
    return result
#####

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        self.time_taken = 0 # This will be calcualted inside the dynamic proof of work code
        self.difficulty = 1 
        self.end_zeros = '0'    # The ending zeros in form of a string
        # self.state = self.get_previous_block()

        # print(f"THE LIST OF NODES in self.nodes is {self.nodes}")


    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def remove_newlines(self,fname):
        flist = open(fname).readlines()
        return [s.rstrip('\n') for s in flist]

####### Implementing dynamic proof of work

    def dynamic_proof_of_work(self, previous_proof):
        check_proof = False
        nonce = 1

        start = time.time()
        while check_proof is False:
            hash_operation = hashlib.sha256(str(previous_proof + nonce).encode()).hexdigest()
            if hash_operation[:self.difficulty] == self.end_zeros:
                check_proof = True
            else:
                nonce += 1
        end = time.time()
        self.time_taken = end-start

        print(f"Time taken to mine the block = {self.time_taken}")

            ## To increase or decrease the difficulty
        if self.time_taken < 10:
            self.difficulty = self.difficulty+1
            self.end_zeros = repeat("0",1,self.difficulty)
        elif self.time_taken >10:
            self.difficulty = self.difficulty-1
            self.end_zeros = repeat("0",1,self.difficulty)

        return nonce

# This function takes a transaction ID as input and returns a signature

    def find_sig_with_trxID(self, given_trxID):
        for i in range(len(self.chain)):
            try:
                for j in range(len(self.chain['chain'][i]['transactions'])):
                    try:
                        if (self.chain["chain"][i]["transactions"][j]['Transaction_ID']) ==given_trxID: 
                            signature = self.chain["chain"][i]["transactions"][j]['Signature']
                        else:
                            signature = ''
                    except Exception as exc:
                        print(exc)
            except Exception as exc:
                print(exc)
        return signature

    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True



    def add_utxo_transaction(self, input, output):
        # First we will create the transaction with the input and output, then create the hash of this transaction
        
        try:
            signature = blockchain.find_sig_with_trxID(input['Previous_Trx_ID'])
        except Exception as exc:
            signature = 'Not Found'

        transaction = ({
                        'Input': {
                                    'Previous_Trx_ID': input['Previous_Trx_ID'],
                                    'Signature':       signature
                                },
                        'Output': output   # This is the address to which the amount should be sent
                        })
        
        trxID = hashlib.sha256(str(transaction).encode()).hexdigest()

        self.transactions.append({
            'Transaction_ID': trxID,
            'Input': input,                 # This is a dictionary again, it has following structure {  'Previous_transaction': transaction_ID, 'Signature': signature} # Here the signature matches the public ID of the previous transcation
            'Output': output                # This is an address to whom the crypto is being sent
        })


####### Now addding a coinbase transaction to it as well.

        output = 50  # Here this 50 represents the 50 bitcoins that are generated in this transaction
        transaction = {
            'Output': output
        }
        trxID_coinbase = hashlib.sha256(str(transaction).encode()).hexdigest()

        trx_signature = Ecdsa.sign(str(transaction), miner_private_key)

        self.transactions.append({
            'Transaction_ID': trxID_coinbase,
            'Output': output,
            'Signature': trx_signature._toString()
        })


        previous_block = self.get_previous_block()
        return previous_block['index'] + 1




    def coinbase_transaction(self):
        output = 50  # Here this 50 represents the 50 bitcoins that are generated in this transaction
        transaction = {
            'Output': output
        }
        trxID = hashlib.sha256(str(transaction).encode()).hexdigest()

        trx_signature = Ecdsa.sign(str(transaction), miner_private_key)

        self.transactions.append({
            'Transaction_ID': trxID,
            'Output': output,
            'Signature': trx_signature._toString()
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length: 
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# Creating a Web App
app = Flask(__name__)

# Creating an address for the node on Port 5001
node_address = str(uuid4()).replace('-', '')


# Creating a Blockchain
blockchain = Blockchain()



@app.route('/inform_nodes', methods =['POST'])
def inform_nodes():
    json = request.get_json(force=True)

    # print(f"\n\nDATA inside json ------{json} \n\n")

    bc_data = json.get('bc_data')
    node_id = json.get('node')

    print(f"Data received from the node {node_id} is: {bc_data}")


    response = {'message': f"Data inside bc_data is {bc_data}"}
    if bc_data is None:
        return "No Data inside bc_data", 400

    # # To update the blocks data on this node
    # node_2 = ['192.168.18.23:5002','192.168.18.23:5003']
    # resp_1 = requests.get(f'http://{node_2[0]}/replace_chain')
    # resp_2 = requests.get(f'http://{node_2[1]}/replace_chain')
    # print(resp_2.text)

    return response, 201

# Get BC state

@app.route('/get_state', methods = ['GET'])
def get_state():
    bc_state = blockchain.get_previous_block()
    response = bc_state
    return jsonify(response), 201

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']

    proof = blockchain.dynamic_proof_of_work(previous_proof)


    if proof != None:
        previous_hash = blockchain.hash(previous_block)
        block = blockchain.create_block(proof, previous_hash)
        response = {'message': 'The block is successfully mined!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    
        return jsonify(response), 200
    else:
        response = {'message': 'Proof not found'}
        return jsonify(response), 400

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Creating a UTXO transaction and adding to the blockchain

@app.route('/add_utxo', methods= ['POST'])
def add_utxo():
    json = request.get_json(force=True)    
    print(f"\n\nDATA inside json ------{json} \n\n")
    transaction_keys = ['Input', 'Output']

    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = blockchain.add_utxo_transaction(json['Input'], json['Output'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201

## Add a single (separate) coinbase transaction to a block 
@app.route('/add_separate_coinbase_trx', methods = ['GET'])
def add_separate_coinbase_trx():
    index = blockchain.coinbase_transaction()
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201



# # Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json(force=True)
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# # Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'Chain is replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'Current chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5001)
