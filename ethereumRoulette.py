__author__ = 'loi'
sub_currency = """
init:
    # Initial: premine 1000000 units to creator
    contract.storage[msg.sender] = 1000000
code:
    # If a message with one item is sent, that's a balance query
    if msg.datasize == 1:
        addr = msg.data[0]
        return (contract.storage[addr])
    # If a message with two items [to, value] are sent, that's a transfer request
    else:
        from = msg.sender
        fromvalue = contract.storage[from]
        to = msg.data[0]
        value = msg.data[1]
        if fromvalue >= value:
            contract.storage[from] = fromvalue - value
            contract.storage[to] = contract.storage[to] + value
            return(1)
        else:
            return(0)
"""
 
import serpent
from pyethereum import transactions, blocks, processblock, utils
processblock.print_debug = 1
 
# compiles serpent into code
code = serpent.compile(sub_currency)
key = utils.sha3('cow')
addr = utils.privtoaddr(key)
#This is to initialize the contract
genesis = blocks.genesis({addr: 10**18 })
 
#The first field is a nonce - to determine the transaction and prevent the replay attack
#The second field is the amount of ether per gas - gas price
#The third field is the start gas
#The forth field is the endowment, don't really know what it is
#The fifth field is the code
tx1 = transactions.contract(0,10**12,10000,0,code).sign(key)
result, contract = processblock.apply_transaction(genesis,tx1)
print ('Initial balance of address %s is: %s' %(addr, str(genesis.get_storage_data(contract, addr))))
 
#Check balance of the address
tx2 = transactions.Transaction(1,10**12,10000,contract,0, serpent.encode_datalist([addr])).sign(key)
result, ans = processblock.apply_transaction(genesis,tx2)
print('Check balance of address %s: %s ' %(addr, str(serpent.decode_datalist(ans))))
 
# Send money
key2 = utils.sha3('cow2')
addr2 = utils.privtoaddr(key2)
tx3 = transactions.Transaction(2,10**12,10000,contract,0,
     serpent.encode_datalist([addr2,500000])).sign(key)
print ('Sending 500000 sub-currency from %s to %s' %(addr, addr2))
result, ans = processblock.apply_transaction(genesis,tx3)
print('Check balance of address %s: %s ' %(addr, str(genesis.get_storage_data(contract, addr))))
print('Check balance of address %s: %s ' %(addr2, str(genesis.get_storage_data(contract, addr2))))
 
while(true):
    #initialize
    wusser = 1;
    flag = false;
    barrel = random.randint(1,6);
    
    #Iterate
    while(True):
        if(wusser == 1):
            print "player one is it...\n"
            raw_input("Spint the barrel!")
            print "The barrel is spinning!...."
            
            rando = random.randint(1,6);
            # the preson was shot!
            if(rando == barrel):
                #Make transaction to another address
                #If you have no currency.. you lose!
                #Reset the game
                break;
    
        if(wusser == 2):
            print "player one is it...\n"
            raw_input("Spint the barrel!")
            print "The barrel is spinning!...."
            
            rando = random.randint(1,6);
            # the preson was shot!
            if(rando == barrel):
                #Make transaction to another address
                #If you have no currency.. you lose!
                #Reset the game
                break;
