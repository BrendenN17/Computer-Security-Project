"""
This file is an example of the logic used to build a blockchain using python

Each new block uses the hash of the previous block
- This means that any changes at any point in the structure will lead to drastically different hash values
- This is how the integrity of the blockchain is verified
"""

#importing library to use SHA-256 hash function
import hashlib

#importing library to decode the QR codes
from PIL import Image
from pyzbar.pyzbar import decode

#importing library to allow me to link user to outside browsers to view block information
import webbrowser

#importing library to help with demo appearance
import time

"""
This class will be the basis for the blockchain

Blocks are initialized with:
- previous block hash value
- current transaction (1 data value per block in my example)
- block data which is a string of the current blocks transaction concatenated with the previous blocks hash
- block hash which uses SHA-2(256bit) hash function to store the hash value of the block data
"""
class Block:

    #Initializes a block to contain data and a hash value based on the transaction information and previous block hash
    # Transaction data is an array of [company, size, location, date]
    def __init__(self, previous_block_hash, transaction_data):
        self.previous_block_hash = previous_block_hash #each block needs the prev block hash value (block its linked to) 
        self.transaction = self.create_transaction(transaction_data) #setting the transaction for the current block
        self.block_data = "!!" + self.transaction + "--" + previous_block_hash #Computing the block data combined with transaction and previous hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()

    # Function creates a transaction(block) with the given data(information) about the single shoe 
    def create_transaction(self, info): #, qr): #adding qr functionality over thanksgiving break
        transaction = str(info)
        return transaction
    


"""
This class will make up the ledger that is the entire blockchain

Functions will include blockchain lookup and adding blocks to chain
"""
class BlockChain:
    blockchain_size = 0 # Tracking size of the chain
    block = Block("START", "START")
    ledger = {}

    prev_block_hash = "START"

    # Function that adds a transaction (block) to the ledger (blockchain)
    # Ledger is a dictionary where keys are block hash values and data is block themselves
    def add_to_chain(self, block):
        self.blockchain_size = len(self.ledger) # Tracking size of the chain
        self.ledger[block.block_hash] = block


    def display_transaction(self):#, key):
        #displays a transaction from the blockchain
        #function just displays the entire ledger of blocks on the blockchain
        print("Current Blockchain Ledger: \n")
        i = 0
        for item in self.ledger.values():
            print("Item: ", i, "is ", item.block_data, "\n")
            i += 1

#Creating the blockchain
blockchain = BlockChain()


"""
Below is an example of my blockchain
I have provided 3 examples of data that would be contained within the individual blocks on the chain
-   Company, style, Size, color, date, Manufactured country, item number

-   In the future the QR code will be implemented and the display function will be changed to a lookup/search function

"""

#Example data for a single shoe (1 block on the blockchain)
t1 = "Nike, Free Runners, 12, Black/Red, 09/16/2009, Antarctica, 1"
t2 = "Puma, Mesh runners, 12.5, White/Gray, 06/08/2020, Switzerland, 2"
t3 = "Converse, Low top skater shoes, 10, Black/Black, 04/25/2012, England, 3"
t4 = "fake"

"""
Adding some example blocks to my blockchain example

These examples will demonstrate 4 examples of how the program works by adding a block
of data to the blockchain.

This data will contain information about a shoe, each of which will be linked through 
a QR code which is decoded for the website containing the shoe information(blocks). 

"""

print("Building the Blockchain with blocks containing bogus information...\n")
print("Hashing blocks with the SHA-2(256bit) hash function...\n")
time.sleep(3)

#Adding block 1 to the chain
initial_block = Block(blockchain.prev_block_hash, t1)
blockchain.add_to_chain(initial_block)


#Adding block 2 to the chain
next_block = Block(initial_block.block_hash, t2)
blockchain.add_to_chain(next_block)

#Adding block 3 (final block) to the chain
final_ex_block = Block(next_block.block_hash, t3)
blockchain.add_to_chain(final_ex_block)


print("Extracting data from QR codes...\n")
time.sleep(3)
#Decoding the QR information for the relevant website string
b1QR = decode(Image.open('QR-codes/Qr1.jpg'))
b1_data = str(b1QR[0].data)
b1_data = b1_data[2:-1]

b2QR = decode(Image.open('QR-codes/qr2.jpg'))
b2_data = str(b2QR[0].data)
b2_data = b2_data[2:-1]

b3QR = decode(Image.open('QR-codes/qr3.jpg'))
b3_data = str(b3QR[0].data)
b3_data = b3_data[2:-1]

#Testing the Fake QR code which is not contained within the blocks of the ledger
#fQR = decode(Image.open('QR-codes/fake-qr.jpg'))
#bf_data = str(fQR[0].data)
#bf_data = bf_data[2:-1]

print("Websites extracted from the QR codes: ")
print(b1_data)
time.sleep(2)
print(b2_data)
time.sleep(2)
print(b3_data)
time.sleep(2)
#print(bf_data)
#time.sleep(2)



"""
Now that all of the blocks have been added to the blockchain ledger,
I can focus on demonstrating the ability for the user to view the information
of the shoes on the blockchain through QR codes.

This will take the user through all 3 QR codes and demonstrate what the user would see.
The system will pause and wait for user command in between QR codes to examine. 
"""

print("Demonstrating the QR code functionality...")
time.sleep(1)

webbrowser.open(b1_data, new=2)
input("press Enter to continue to the next block...\n")
webbrowser.open(b2_data, new=2)
input("press Enter to continue to the final block...\n")
webbrowser.open(b3_data, new=2)
input("press Enter to continue to displaying the ledger...\n")


#Displaying all the blocks within the ledger
blockchain.display_transaction()

"""
Future work that could be done:

- Implementing a lookup feature which would be needed once the ledger reaches a bigger size

- It would also be nice for in the future, rather than hardcoding a fake QR code, 
the hope would be that a function could be written to verify the authenticity of the QR information,
and checking with the blockchain database to determine whether the shoe is authentic or possibly fake.
(This would help add to the security and integrity of the project)
"""