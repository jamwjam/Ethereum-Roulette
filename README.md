Created by Jung Kim, Richard Rice, Luc Nguyen, Ricardo Barrera

#Prerequisites


1. https://docs.google.com/document/d/1jybBJRoq0E3V-ew2zdhf6hg8w855tJagBxm_se3flJ8/edit
2. sudo apt-get install python-tk

#Introduction

Ethereum Roulette brings forth the traditional game of Russian roulette for the millennial generation to enjoy with convenience. Instead of tragedy as an outcome, Ethereum Roulette is an exciting and dignified way to win crypto-currency fast! 

#Implementation

In the implementation, our program is initialized by placing the ‘bullet’ one of the six empty barrels possible in the gun. Two players alternate, shooting themselves, hoping that their trigger does not fire the bullet. If the bullet is fired, the struck player loses the current round and must give 5000 sub-currency to the other player. Else, the player hands the gun to the opponent for them to fire. Thus, the cycle repeats until one player either forfeits out of the game, or play until their sub-currency funds run out.

#Security Analysis

There were potential security concerns that had to be handled upon the completion of Ethereum Roulette. One major concern upon implementing our code was a possoible buffer overflow attack, as we initially aimed to develop our program with the ethereum cpp client (cpp-ethereum). With numerous user input that exists on the program, it allows potential attackers to provide input that would overflow malicious lines of executable code into the device’s adjacent memory. This was handled by deciding to develop the ethereum project not on the cpp-ethereum platform, but its python counterpart, Pyethereum. Buffer overflow attacks, as the attacks mainly rely on access on memory and ambiguous data types. As python utilizes an interpreter as well as fixating data types automatically, and having no direct access to memory, it is inherently safe from buffer overflow attacks. 
