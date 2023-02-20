from web3 import Web3
from flask import Flask, jsonify, request, render_template

import requests
# from web3.auto import w3
import json

# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
# address = '0x893eB423C322a4BA6E9619582E30e884bb9CFD09'
# balance_in_wei = w3.eth.get_balance(address)
# balance_in_ether = w3.from_wei(balance_in_wei, 'ether')
# print('Balance of ', address, 'is', balance_in_ether, 'ETH')

# private_key = '0xce74ba56c5df8563d65af5a072a8c4f6af9e60c8b911533dd4aa491deb75fe2b'
# sender_address = '0x893eB423C322a4BA6E9619582E30e884bb9CFD09'
# recipient_address = '0xCE0eB7762e4A34db365f66589d6288d16Bd3AC93'

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
app = Flask(__name__)

# class API:
#     def __init__(self, base_url):
#         self.base_url = base_url

#     def get(self, endpoint, params=None):
#         url = self.base_url + endpoint
#         response = requests.get(url, params=params)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return 400


def getBalance(address):
    return web3.from_wei(web3.eth.get_balance(address), 'ether')


def getAccounts():
    return web3.eth.accounts


def getPrivateKey():
    file_key = open('PK.txt', 'r')
    readData = file_key.read()
    data_in_file = readData.replace('\n', '').split('')
    file_key.close()
    return data_in_file


def getAccountPair():
    keys = getPrivateKey()
    account = getAccount()
    getPPK = []
    i = 1
    for x in account:
        getPPK.append({
            'Account': x, 'Key': keys[1]
        })
        i = i+2
    return json.dumps(getPPK)


def transfer(sender_address, recipient_address,keys,ether):
    transaction = {
        'to': recipient_address,
        'value': web3.to_wei(ether, 'ether'),
        'gas': 21000,
        'gasPrice': web3.to_wei('50', 'gwei'),
        'nonce': web3.eth.get_transaction_count(sender_address),
    }
    signed_txn = web3.eth.account.sign_transaction(transaction, keys)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.to_hex(tx_hash)



# api = API('http://127.0.0.1:5000')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get_accounts")
def getAccount():
    return getAccountPair()


@app.route("/get_balance" , methods=['POST'])
def getBalance():
    data = request.json
    message = {
        'status' : 'success',
        'ether' : getBalance(data['address'])
    }
    return jsonify(message), 200


@app.route("/transfer", methods=['POST'])
def data_transfer():

    data = request.json,
    massege = {
        'status' : 'Transfer Success',
        'hash': transfer(data['tx'],data['key'],data['ether'],data['rx'])
    }
    return jsonify(massege), 200


if __name__ == "__main__":
    app.run(debug=True)
