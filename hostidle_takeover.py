import time
import numpy as np
import os
import math

class Hostidle_Takeover(object):

#   This is an idle game wherein you passively accrue money, which you can use to purchase shares of a company, 
#   which will earn you dividends, through which you hope to buy out the entire company. 
#   If I wanted to expand on this game, I would make money a global variable, and allow the user to instantiate
#   any number of companies (the class would be a single company instead of the entire game), with randomized values
#   for total shares and starting share price. The user would then be able to select which company to run each command on.
#   Another possible thing to implement is the impact on the price of buying or selling a huge amount of sales, but I feel
#   like that would go against the theme of "one person cannot make a difference".
   
    def __init__(self, money = 0, shares = 0, price = 500, total = 250):
        self.money = money   # Amount of money the player has. By default increases by 100 per second.
        self.shares = shares # Number of shares the player has.
        self.price = price   # Current price of a single share.
        self.total = total   # Total number of purchasable shares.
        self.dividends = 0   # Amount of money the player passively receives per second from shares.
        self.current_time = int(time.time())                       # Time value at last time check.
        self.time_change = int(time.time()) - self.current_time    # Number of seconds from last time check to current time check.
        self.END = False     # Is the ending reached?
        
        
    def price_change(self):   # the share price varies in time

        for i in range(self.time_change):    # share price will change every second according to a normal distribution from the current price
                                        # this should allow for variability but also occasional stretches of above or below average prices that a perceptive player can exploit
            self.price = round(self.price + 5*np.random.normal())    
            if self.price < 1:               # the share price cannot be 0 or negative, no matter how bad the company does
                                             # I'm not going to be implementing bankrupcty as a failure state
                self.price = 1
   #     print("Share price is now", price)   #uncomment this to see how the share price changes every second


    def progress(self):     # progresses the game between user inputs 

        print("Awaiting orders:")
        self.order = input("> ")   
        self.order = self.order.lower()       # the lower() function changes input to lowercase in case the player writes sarcastically or has a stuck caps lock key
        self.time_change = int(time.time()) - self.current_time
        self.dividends = int(0.02*self.shares*self.price*self.time_change)
        self.current_time = int(time.time())
        
    #    print(self.time_change,"seconds have passed. You get", self.dividends,"rubles from dividends!") # Uncomment this to see exactly how much money you get from dividends
        self.money += 100*self.time_change + self.dividends
    
        self.price_change() # calls the share price to vary in time
        

        
    def info(self):   # Gives information about the state of the game.
        print("You have",self.money,"rubles and",self.shares,"shares out of",self.total,"total shares available for purchase.")
        print("The current share price is",self.price,"and each gives out",int(0.02*self.price),"rubles per second in dividends.")
        print("Your passive income is",100 + int(0.02*self.price)*self.shares,"rubles per second.")
          
    def buy(self):    # Allows the player to buy shares.
        print("You have",self.money,"rubles and the price of a share is",self.price,"rubles.")
        max_purchase = math.floor(self.money/self.price)
        if max_purchase + self.shares > self.total:    # can't purchase more than the total amount of shares
            max_purchase = self.total - self.shares
        print("How many would you like to buy? It seems you can afford to buy up to", max_purchase, "shares.")
        purchase = input("> ")     # purchase is a temporary variable local to this function, indicating how many shares the player wants to buy
        if purchase.isdigit():   # sanitizing user input
            purchase = int(purchase)
            if purchase > 0 and purchase <= max_purchase:
                self.shares += purchase
                self.money -= purchase*self.price
                print("Successful purchase of",purchase,"shares for",purchase*self.price,"rubles. You now have",self.shares,"shares.")
            elif purchase == 0:
                print("Okay, you're just browsing, that's fine too.")
            else:
                print("You can't buy that many shares.")
        else:
            print("Unsuccessful purchase.")
        
        if self.shares >= self.total:
            self.shares = self.total
            self.END = True
    
    def sell(self):   # Allows the player to sell shares.
        print("You have",self.shares,"shares and the price of a share is",self.price,"rubles.")
        print("How many would you like to sell?")
        sale = input("> ")
        if sale.isdigit():
            sale = int(sale)
            if sale > 0 and sale <= self.shares:
                self.shares -= sale
                self.money += sale*self.price
                print("Successful sale of",sale,"shares for",sale*self.price,"rubles. You now have",self.shares,"shares.")
            elif sale == 0:
                print("You're right, it's better to hold on to these.")
            else:
                print("You can't sell that many shares.")
        else:
            print("Unsuccessful sale.")
            
    def help(self): # Prints out the list of commands.
        print("info - tells you your current bank balance, and provides information about shares")
        print("buy - purchase shares with your hard earned money")
        print("sell - sell shares to gain a profit or loss on investment")
        print("quit - ends the game")
        print("help - you now know what this does")
        print("The first letter of any command can also be used as a shortcut.")

print("Welcome to Hostidle Takeover, the text-based idle game where you dream about quitting your job and taking over a company.")
print("Write help to get a list of commands.")
print("")

game = Hostidle_Takeover()      # creates an instance of the game with default values
                                # 0, 0, 500 are the default starting values for money, shares, and price

while(True):


        
    if game.END == True:
        print("Congratulations, capitalist! You have successfully bought every available share of the company.")
        print("Unfortunately for you, the original founder only released 49% as part of the Initial Public Offering,  so you do not get to take over control.")
        print("How anticlimactic!")
        print("At least you are now able to safely quit your day job and stop worrying about money.")
        print("You retire with",game.money,"rubles in savings,",game.shares,"shares, and a pension of",int(0.02*game.shares*game.price),"rubles per second.")
        print("Thanks for playing!")
        break

    game.progress()
    
    if game.order == "info" or game.order == "i":
        game.info()

    elif game.order == "help" or game.order == "h":
        game.help()
        
    elif game.order == "quit" or game.order == "q":   # ends the game prematurely
        print("I understand, this life is not for everyone.")
        print("You retire with",game.money,"rubles in savings,",game.shares,"shares, and a pension of",int(0.02*game.shares*game.price),"rubles per second.")
        break       

    elif game.order =="hi" or game.order =="hello" or game.order =="greetings" or game.order =="howdy":
        print("Yeah hi but do actually write help to get a list of commands. This is not really processing natural language.")
    elif game.order =="bye" or game.order =="goodbye" or game.order == "badbye":
        print("If you want to quit, just say so, I won't judge! Clear communication is important.")
        
    elif game.order == "buy" or game.order == "b":
        game.buy()
    elif game.order == "sell" or game.order =="s":
        game.sell()
    else:
        print("Write help to get a list of commands.")
    print("")