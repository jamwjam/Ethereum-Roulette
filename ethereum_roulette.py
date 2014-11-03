
#Authors: James Kim, Luc Nguyen, Ricardo Barrera, Richard Rice
#CMSC 414: Russian Roulette

import Tkinter
from Tkinter import *
from ttk import Button, Style
import serpent
from pyethereum import transactions, blocks, processblock, utils
import random, sys, time

russian_roulette = """
init:
    # Initial: premine 10000 units to both players. 0 is player 1 
    # and 1 is player 2
    contract.storage[0] = 10000
    contract.storage[1] = 10000
code:
    # If a message with one item is sent, that's a balance query
    if msg.datasize == 1:
        player = msg.data[0] # This is the first element in the encoded datalist
        return (contract.storage[player])
    # If a message with two items [from, to] are sent, that's a transfer request. Each transfer
    # is of value 2000
    else:
        from = msg.data[0] # The player who is sending money
        fromvalue = contract.storage[from] # Sender's balance
        to = msg.data[1] # The player who is receiving money
        tovalue = contract.storage[to] # Recipient's balance
        money = 5000 # The money to receive. I set it low so the game doesnt 
                     # last so long
        if fromvalue >= money: #make sure there is enough funds
            contract.storage[from] = fromvalue - money #take funds away
            contract.storage[to] = tovalue + money # add funds
            return(1)
        else: #player doesnt have enough, therefore he is the loser
            return(0)
"""

flag = -1
ans = 0
ans2 = 0
barrel = random.randint(1,6)
#keep track of the nonces
p1_nonce = 2
p2_nonce = 1
contract = 0
key = 0
key2 = 0
wusser = 1
genesis = 0


class RouletteFrame(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent, background="gray")   
		self.parent = parent
		self.initUI()

	def initUI(self):
		global ans, ans2
		self.parent.title("Ethereum Roulette")
		self.style = Style()
		self.style.theme_use("default")
		self.pack(fill=BOTH, expand=1)
		self.playerButt = Button(self, text="Click to take the shot", command=self.shoot)
		self.playerButt.place(x=0, y=0)
		self.wussButt = Button(self, text="Click to wuss out!", command=self.wussout)
		self.wussButt.place(x=235, y=0)
		self.txt = Text()
		self.txt.insert(Tkinter.END, 'Player 1 initial balance is: %s\n' %(str(serpent.decode_datalist(ans))));
		self.txt.insert(Tkinter.END, 'Player 2 initial balance is: %s\n' %(str(serpent.decode_datalist(ans2))));
		self.txt.configure(state=Tkinter.DISABLED)
		self.txt.place(x = 0, y = 22)
		print("Player 1's turn...");
		self.txt.insert(Tkinter.END, "\nPlayer 1's turn...");

	def load_dots(self, dot_count):
		for i in range(dot_count):
			sys.stdout.write(".") 
			sys.stdout.flush() 
			time.sleep(.2)
		print 

	def print_with_dots(self, s, dot_count):
		print s,
		self.load_dots(dot_count)
	
	def wussout(self):
		if(wusser == 1):
			print("\n\nPlayer 1 wussed out!");
			print("***************************************");
			print("*	    Player 2 won!	     *");
			print("***************************************");
		else:
			print("\n\nPlayer 2 wussed out!");
			print("***************************************");
			print("*	    Player 1 won!	     *");
			print("***************************************");

		time.sleep(2)
		exit();
		

	def gameover(self):
		if(flag == 1):
			print("***************************************");
			print("*	    Player 1 won!	     *");
			print("***************************************");
		else:
			print("***************************************");
			print("*	    Player 2 won!	     *");
			print("***************************************");
		time.sleep(2)
		exit();

	def shoot(self):
		global p1_nonce, p2_nonce, contract, key, key2, wusser, genesis, flag, barrel
		rando = random.randint(1,6);
		self.txt.configure(state=Tkinter.NORMAL)
		self.txt.delete(0.0, Tkinter.END)
		if(wusser == 1):
			self.print_with_dots("\tThe barrel is spinning",5)
			if(rando == barrel):
				barrel = random.randint(1,6)
				print("Bang! You lost this round!");
				self.txt.insert(Tkinter.END, "Bang! You lost this round!");
				time.sleep(.5)
				tx4 = transactions.Transaction(p1_nonce,10**12,10000,contract,0,serpent.encode_datalist([0,1])).sign(key)
				result, ans = processblock.apply_transaction(genesis,tx4);
			
				if(genesis.get_storage_data(contract,0) == 0): #player doesnt have enough money
				    flag = 2;
				    print("\tPlayer 1 has no more funds")
				    self.gameover();
				else:
				    print('\tPlayer 1 now has : %s and Player 2 now has: %s ' % (str(genesis.get_storage_data(contract,0)),str(genesis.get_storage_data(contract,1))))
				    p1_nonce = p1_nonce + 1;
		    		time.sleep(.4)
			else:
				print("\tThe barrel was empty!")
				time.sleep(.5)
				self.txt.delete(0.0, Tkinter.END)
			self.txt.insert(Tkinter.END, "\nPlayer 2's turn...");
			print("\nPlayer 2's turn...");
			wusser = 2;
		elif(wusser == 2):
			self.txt.insert(Tkinter.END, "Player 2's turn...\n")
			self.print_with_dots("\tThe barrel is spinning",5)
			# the person was shot!
		    	if(rando == barrel):
				barrel = random.randint(1,6)
				print("Bang! You lost this round!");
				self.txt.insert(Tkinter.END, "Bang! You lost this round!");
				time.sleep(.5)
				tx5 = transactions.Transaction(p2_nonce,10**12,10000,contract,0,serpent.encode_datalist([1,0])).sign(key2)
       			 	result, ans = processblock.apply_transaction(genesis,tx5);
				if(genesis.get_storage_data(contract,1) == 0): #player doesnt have enough money
				    flag = 1;
				    print("\tPlayer 2 has no more funds")
				    self.gameover();
				else:
				    print('\tPlayer 1 now has : %s and Player 2 now has: %s ' % (str(genesis.get_storage_data(contract,0)),str(genesis.get_storage_data(contract,1))))
				    p2_nonce = p2_nonce + 1;
            			time.sleep(.4)
	  	 	else:
				print("\tThe barrel was empty!")
				time.sleep(.5)
				self.txt.delete(0.0, Tkinter.END)
			self.txt.insert(Tkinter.END, "\nPlayer 1's turn...");
			print("\nPlayer 1's turn...");
			# set up for the next player
            		wusser = 1; 
		
		self.txt.configure(state=Tkinter.DISABLED)

def stopExit():
	print "Cannot close!"

def main():
	global ans, ans2, contract, key, key2, genesis
	# compiles serpent into code
	code = serpent.compile(russian_roulette)
	#player1
	key = utils.sha3('Bob')
	addr = utils.privtoaddr(key)
	#player2
	key2 = utils.sha3('Joe')
	addr2 = utils.privtoaddr(key2)

	#This is to initialize the block
	genesis = blocks.genesis({addr: 10**18 , addr2: 10**18})

	#The first field is a nonce, gas price, start gas, endowment, code
	#initialize the contract
	tx1 = transactions.contract(0,10**12,10000,0,code).sign(key)
	result, contract = processblock.apply_transaction(genesis,tx1)

	#Check balance of player 1
	#encode_datalist(array) is the data array that is represented in msg.data
	tx2 = transactions.Transaction(1,10**12,10000,contract,0, serpent.encode_datalist([0])).sign(key)
	result, ans = processblock.apply_transaction(genesis,tx2)
	#serpent.decode_datalist(ans) is one way to get return or we can directly access the contracts 

	#Check balance of player 2
	tx3 = transactions.Transaction(0,10**12,10000,contract,0, serpent.encode_datalist([1])).sign(key2)
	result, ans2 = processblock.apply_transaction(genesis,tx3)

  	#initialize 
	root = Tk()
	root.geometry("350x75+750+350")
	root.protocol("WM_DELETE_WINDOW", stopExit)
	app = RouletteFrame(root)
    	root.mainloop() 


if __name__ == '__main__':
    main()  


