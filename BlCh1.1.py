import datetime
import hashlib
import json
from flask import Flask, jsonify

class BlockChain_1:
    
    def __init__(self):
        self.chain = []
        self.createBlock(proof=1, prev_hash='0')
        
    def createBlock(self, proof, prev_hash):
        Block = {'index': len(self.chain)+1,
                  'time': str(datetime.datetime.now()),
                   'proof': proof,
                   'prev_hash': prev_hash }
        self.chain.append(Block)
        return Block
    def last_block(self):
        return self.chain[-1]
     
    def proof_of_work(self,prev_proof):
        new_proof = 1
        checkProof = False
        while checkProof == False:
            hashOP = hashlib.sha256(str(new_proof**2 - prev_proof**2).encode()).hexdigest()
            if hashOP[:4] == '0000':
                checkProof = True
            else:
                new_proof += 1
        return new_proof
    
    def find_Hash(self,block):
        encryptedBlk = json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encryptedBlk).hexdigest()
    
    def chainValidation(self, chain):
        previous_block = chain[0]
        blockIndex = 1
        while blockIndex <len(chain):
            block = chain[blockIndex]
            if block['prev_hash']!= self.find_Hash(previous_block):
                return False
            proof = block['proof']
            prevproof = previous_block['proof']
            hashOP = hashlib.sha256(str(proof**2 - prevproof**2).encode()).hexdigest()
            if hashOP[:4]!='0000':
                return False
            previous_block = block
            blockIndex += 1
        return True

#creating web

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockChain = BlockChain_1()

@app.route('/mineBlock', methods = ['GET'])
def mineBlock():
    prevBlk = blockChain.last_block()
    prevproof = prevBlk['proof']
    proof = blockChain.proof_of_work(prevproof)
    prevHash = blockChain.find_Hash(prevBlk)
    Blockx = blockChain.createBlock(proof, prevHash)
    response = { 'message': 'You mined a block!!', 
                 'Index': Blockx['index'],
                 'TimeStamp': Blockx['time'],
                 'nonce': Blockx['proof'],
                  'previous_Hash': Blockx['prev_hash'] }
    return jsonify(response), 200

@app.route('/getChain', methods = ['GET'])
def getChain():
    Chain = {'chain':blockChain.chain,
             'Length Of Chain': len(blockChain.chain)}
    return jsonify(Chain), 200

@app.route('/isvalid', methods = ['GET'])
def isvalid():
    valid = blockChain.chainValidation(blockChain.chain)
    if valid:
        reply = {
            'message': 'The Blockchain is vallid'}
    else:
        reply = {
            'message' : 'Oops! The Blockchain is not valid'}
    return jsonify(reply), 200

app.run(host='0.0.0.0', port= 5000)