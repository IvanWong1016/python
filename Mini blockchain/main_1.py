#main_1.py

import requests
import os
import json
import pandas as pd
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.privateKey import PrivateKey
from ellipticcurve.privateKey import PublicKey


# Change this address according to the address in the flask server. 
port = "5001"
ip = "192.168.1.178"  # This IP needs to change according to the local IP presented by your flask server
node = f"{ip}:{port}"


def write_bc_to_disk(data):
    with open('bc_ledger_data.json', 'w') as f:
        json.dump(eval(data), f)


# This command will run our BC node in a separate cmd
for i in range(1,4):
    os.system(f"start cmd /k python BC_node_{i}.py")


time.sleep(3)

# To connect all the nodes
nodes_data = json.load(open('nodes.json','r'))
node_connect_response = requests.post(f'http://{node}/connect_node', data= json.dumps(nodes_data))


# The following commands will show the menu to choose from 
while(True):
    print("Blockchain Assignment\n\n")


    print("a: Add UTXO Transaction")
    print("b: Add single Coinbase Transaction")
    print("c: View all Blocks")
    print("d: View all Transactions in each block")
    print("e: Generate a Public and Private Key pair")

    print("f: Print the BC state")
    
    print("g: Get blocks from other nodes")
    print("h: Inform other nodes what blocks or transactions it has")

    print("i: Show the connected nodes")
    print("j: Show the Current Node")
    
    print("k: Exit")
    option = input("Select your option:   ")

### ADD UTXO transaction

    if option =="a":
        print("\n\nOption a is selected")

        # This will get the private key from the user and create a private key object out of it 
        priv_key_get = input("Please enter your private key:  \n\n")
        print('\n')
        private_key = PrivateKey.fromString(priv_key_get)

        # This will get the public key from the user and create a public  key object out of it 

        pub_key_to_send_get = input("Please enter the recepient Public Key:  \n\n")
        public_key = PublicKey.fromString(pub_key_to_send_get)
        print('\n')
        # This will get the Transaction ID of the previous transaction to which this transaction is related
        prev_trx_ID = input("Please enter the previous transaction ID:  \n\n")
        print('\n')
        signature = Ecdsa.sign('the transaction', private_key)  # The signature should match the public key in the previous transaction
        
        get_input = {
                'Previous_Trx_ID': prev_trx_ID,
                'Signature': signature.toDer().hex()
                }


        data_to_upload = {"Input":get_input,"Output":public_key.toString()}
        response = requests.post(f'http://{node}/add_utxo', data= json.dumps(data_to_upload))
        mineRequest = requests.get(f'http://{node}/mine_block')
        print(f"\n\n {mineRequest.text}")
        print('\n')


# For writing bc data to disk
        response_2 = requests.get(f'http://{node}/get_chain')
        write_bc_to_disk(response_2.text)


## To add a single Coinbase transaction
    elif option == "b":
        print("\n\nOption b is selected")
        print("\n\n  Adding only a coinbase transaction to the block")
        response = requests.get(f'http://{node}/add_separate_coinbase_trx')        
        mineRequest = requests.get(f'http://{node}/mine_block')
        print(f"\n\n {mineRequest.text}")        
        print(f"\n\n Response = {response.text}")

# For writing bc data to disk
        response_2 = requests.get(f'http://{node}/get_chain')
        write_bc_to_disk(response_2.text)


    elif option =="c":
        print("\n\nOption c is selected")
        # Get all the blocks from the Blockchain by using requests library
        response = requests.get(f'http://{node}/get_chain')
        print(response.text)

### This will get all the transactions from the existing blocks        
    elif option =="d":
        print("\n\nOption d is selected")
        # Get all the transactions from the existing blocks
        nodes_data = json.load(open('nodes.json','r'))
        node_connect_response = requests.post(f'http://{node}/connect_node', data= json.dumps(nodes_data))
        resp_1 = requests.get(f'http://{node}/replace_chain')
        response = requests.get(f'http://{node}/get_chain')
        
        data_in_json = json.loads(response.text)
        required_data = data_in_json['chain']
        for i in range(len(required_data)):
            print(required_data[i])

## This will generate a public and private key pair to test out the program
    elif option == "e":
        test_priv_key =PrivateKey()

        print(f"Private Key: {test_priv_key.toString()} ")
        print(f"Public Key: {test_priv_key.publicKey().toString()} ")



## To get BC state
    elif option == "f":
        response = requests.get(f'http://{node}/get_state')
        print(response.text)

## To get blocks from other nodes

    elif option == "g":

        while(True):
            print("Select your node \n\n")
            print("a:  Node 1 = 5001 (default option)")
            print("b:  Node 2=  5002")
            print("c:  Node 2=  5003")
            print("d:  Go back to Main Menu")


            option_2 = input("Enter your options from above: \n")

            if option_2 == "a":
                port = 5001
                node = f"{ip}:{port}"
                response = requests.get(f'http://{node}/get_chain')
                print(f" The block data in node: {node}\n\n{response.text}")
            elif option_2 == "b":
                port = 5002
                node = f"{ip}:{port}"
                response = requests.get(f'http://{node}/get_chain')
                print(f" The block data in node: {node}\n\n{response.text}")
            
            elif option_2 == "c":
                port = 5003
                node = f"{ip}:{port}"
                response = requests.get(f'http://{node}/get_chain')
                print(f" The block data in node: {node}\n\n{response.text}")
            elif option_2 == "d":
                break

## To inform other nodes

    elif option == "h":
        response = requests.get(f'http://{node}/get_chain')
        bc_data = {'bc_data': json.loads(response.text), 'node': node}
        port_array = ['5001','5002','5003']
        if port == '5001':
            port_array = ['5002','5003']
        elif port =='5002':
            port_array = ['5001','5003']
        elif port =='5003':
            port_array = ['5001','5002']

        for port in port_array:
            node_2 = f"{ip}:{port}"
            nodes_data = json.load(open('nodes.json','r'))
            node_connect_response = requests.post(f'http://{node_2}/connect_node', data= json.dumps(nodes_data))
            inform_response = requests.post(f'http://{node_2}/inform_nodes', data=json.dumps(bc_data))
            resp_1 = requests.get(f'http://{node_2}/replace_chain')

  

        print(f'Response from inform_response: {inform_response.text}')





# To show the connected nodes
    elif option == "i":
        node_connect_response = requests.post(f'http://{node}/connect_node', data= json.dumps(nodes_data))
        print(node_connect_response.text)

# To show current node
    elif option == "j":
        print(f"The current node is : {node}")

# To exit the program
    elif option =="k":
        print("\n\nExiting....")
        exit()
    else:
        print("\n\nInvalid option selected, please try again")


