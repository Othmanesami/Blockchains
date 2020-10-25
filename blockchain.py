import hashlib
from time import time
import json



class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #create the genesis block
        self.new_block(previous_hash = 1, proof= 100)

    def new_block(self, proof, previous_hash= None):
        """
        create a new block in the blockchain
        :param proof: <int> the proof given by the proof of work algorithm
        :param previous_hash: (Optional) <str> hash of previous block
        :return: <dict> new block
        """
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transaction' : self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1])
        }

        #reset the list of new transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go to the next mined block
        :param sender: <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> Amount
        :return: <int> the index of the block that will hold this transaction
        """

        self.current_transactions.append({
            'sender' : sender,
            'recipient' : recipient,
            'amount' : amount
        })

        return self.last_block['index'] + 1


    @staticmethod
    def hash(block):
        """
        creates a sha-256 hash of a block
        :param block: <dict> block
        :return: <str>
        """
        #we must make sure that the dictionary is ordered or we will have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]