import random


class agent:
    def __init__(self, id, cash,shares=0):
        self.id= id
        self.cash = cash
        self.shares = shares #持有股份

    def buy(self,now_price):
        share = random.randint(1,10) #买1-10手
        price = now_price+0.01
        if self.cash<price*share*100:
            print('{}余额不足，无法购买！'.format(self.id))
        else:
            self.cash -= price * share * 100
            action_buy = [share,price,self.id]
        return action_buy
    def update(self,share,price=0): #正数为买，负数wei
        self.shares+=share
        if share<0:
            self.cash+=share*100*price  #现金增加
    def sell(self,now_price):
        share = random.randint(1, 10)  # 卖1-10手
        price = now_price - 0.01
        action_sell = [-share,price,self.id]






