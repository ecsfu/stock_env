import random


class agent:
    def __init__(self, id, cash,shares=0,now_price,env):
        self.id= id
        self.cash = cash
        self.env = env
        self.shares = shares #持有股份
        self.now_price = now_price
    def buy(self):
        share = random.randint(1,10) #买1-10手
        price = self.now_price+0.01
        if self.cash<price*share*100:
            print('{}余额不足，无法购买！'.format(self.id))
        else:
            action_buy = [share,price,self.id]
        return action_buy

