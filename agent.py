import random


class agent:
    def __init__(self, id, cash,shares=0,now_price,env):
        self.id= id
        self.cash = cash
        self.env = env
        self.shares = shares
        self.now_price = now_price
    def buy(self):
        share = random.randint(1,10)
        price =

