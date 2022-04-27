import gym
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from gym import spaces
from gym.utils import seeding
from stable_baselines3.common.vec_env import DummyVecEnv
import time
matplotlib.use("Agg") #控制绘图不显示，必须在import matplotlib.pyplot as plt前运行

# from stable_baselines3.common.logger import Logger, KVWriter, CSVOutputFormat


class StockTradingEnv(gym.Env):
    """"""
    """
    -------
   
    step()
    返回当前交易得到的价格及订单列表
    _update() 
    #比较pre买卖列表 与当前买卖列表的差异，对于有变化的订单根据用户id将成交信息反回给用户
       

    _list_clear() 
    #删除买卖列表中股份为0的订单
    """

    metadata = {"render.modes": ["human"]}

    def __init__(   #定义一只股票的交易环境
        self,
        tradable_shares,   #流通股本
        initial_price, #初始交易价格
        price_limiting,#涨跌限制

        # initial_amount,
        buy_cost_pct,   #买入费率
        sell_cost_pct,  #卖出费率

        state_space, #状态空间 [tradable_sharesx1 ,now_pricex1,pre_closex1,list_of_buy ,list_of_sell] ->
        action_space, #动作空间,[sharesx1,bid_ask_pricex1,user_id]  ->3


    ):

        self.tradable_shares = tradable_shares
        self.now_price  = initial_price
        self.pre_close = initial_price
        self.list_of_buy = []
        self.list_of_sell = []
        self.pre_list_of_buy = []
        self.pre_list_of_sell = []
        self.volum = 0 #交易量

        self.price_limiting = price_limiting
        self.buy_cost_pct = buy_cost_pct
        self.sell_cost_pct = sell_cost_pct

        self.state_space = state_space
        self.action_space = action_space

        self.action_space = spaces.Box(low=-1, high=1, shape=(self.action_space,)) #动作空间
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(self.state_space,)
        )

        self.terminal = False

        # initalize state
        self.state = self._initiate_state() #初始化状态

        # initialize reward

        self._seed()


    def step(self, actions):
        self.terminal = False #终止条件,暂未考虑
        time.sleep(0.0001)
        now_time = time.time()
        print('now_time',now_time)
        actions.append(now_time) #增加时间戳[shares,b_or_s ,user,time]

        if self.terminal:
            # print(f"Episode: {self.episode}")
            pass
        else:
            if actions[1]>self.pre_close*(1+self.price_limiting) or actions[1]<self.pre_close*(1-self.price_limiting):
                print('超出涨跌限制，挂单作废.....')
                return None,None,None # 超出涨跌限制
            elif actions[0]<0: #卖出
                if isinstance(self.list_of_sell,np.ndarray):

                    self.list_of_sell = self.list_of_sell.tolist()

                self.list_of_sell.append(actions)
                self.list_of_sell = np.array(self.list_of_sell)
                self.list_of_sell = self.list_of_sell[self.list_of_sell[:,1].argsort()] #按价格进行排序从小到大
            elif actions[0]>0:#买入
                if isinstance(self.list_of_buy,np.ndarray):
                    self.list_of_buy = self.list_of_buy.tolist() #转列表
                self.list_of_buy.append(actions)
                self.list_of_buy = np.array(self.list_of_buy) #转numpy
                self.list_of_buy = self.list_of_buy[self.list_of_buy[:, 1].argsort()[::-1]]  # 按价格进行排序从大到小
            """连续竞价交易制度：
            1. 最高买进申报与最低卖出申报相同，则该价格即为成交价格；
            2. 买入申报价格高于即时揭示的最低卖出申报价格时，以即时揭示的最低卖出申报价格为成交价；
            3.卖出申报价格低于即时揭示的最高买入申报价格时，以即时揭示的最高买入申报价格为成交价
                     sell
                     ---------- 
                     buy                                                    
            
            """
            if len(self.list_of_sell)==0  or len(self.list_of_buy)==0: #任一列表为空，返回
                print('无买单或卖单，挂单中...')
                return None,None,None #无法成交
            i = 0
            print(self.list_of_sell[0][4],self.list_of_buy[0][4])
            print(self.list_of_sell[0][4]== self.list_of_buy[0][4])
            if self.list_of_sell[0][4]>self.list_of_buy[0][4]: #卖单后入
                print('新入卖单，开始匹配买单...')
                if self.list_of_sell[0][1]<self.list_of_buy[0][1]: #卖价低于买价，可交易
                    print('新入卖单价格低于买单价格，可以成交...')
                    while i<len(self.list_of_buy) and -self.list_of_sell[0][0] >0:
                        print('匹配第{}个买单'.format(i+1))
                        if self.list_of_sell[0][1] < self.list_of_buy[i][1]: #可交易
                            print('卖单价格低于第{}个买单，可以成交'.format(i+1))
                            if -self.list_of_sell[0][0] <= self.list_of_buy[i][0]: #卖单小于买单
                                print('卖单小于买单')
                                self.list_of_buy[i][0]+=self.list_of_sell[0][0] #更新买单
                                self.list_of_sell[0][0]=0#清卖单
                                self.now_price = self.list_of_buy[i][1]  # 更新成交价格
                                print('agent{}直接卖单成交，成交价格{}'.format(self.list_of_sell[0][2],self.now_price))
                            else:#卖单大于于买单
                                print('卖单大于买单')
                                self.list_of_sell[0][0]+=self.list_of_buy[i][0]#更新卖单
                                self.list_of_buy[i][0]=0 #清买单
                                self.now_price = self.list_of_buy[i][1]  # 更新成交价格
                                print('agent{}买单全部分成交，成交价为{}'.format(self.list_of_buy[i][2], self.now_price))
                                print('agent{}卖单部分成交，成交价为{}'.format(self.list_of_sell[0][2],self.now_price))

                        i+=1

            i=0
            if self.list_of_sell[0][4]<self.list_of_buy[0][4]: #买单后入
                print('新入买单，开始匹配卖单...')
                if self.list_of_sell[0][1]<self.list_of_buy[0][1]: #买价高于卖价，可交易
                    print('新入买单价格高于卖单价格，可以成交...')
                    while i<len(self.list_of_sell) and self.list_of_buy[0][0] >0: #买单没有全部成交或卖单没有全部遍历
                        print('匹配第{}个卖单'.format(i + 1))
                        if self.list_of_sell[i][1] < self.list_of_buy[0][1]: #可交易
                            print('买单价格高于第{}个卖单，可以成交'.format(i + 1))
                            if self.list_of_buy[0][0] <= -self.list_of_sell[i][0]:  #买单小于卖单的量
                                self.list_of_sell[i][0]+=self.list_of_buy[0][0] #卖单更新
                                self.list_of_buy[0][0]=0 #清买单
                                self.now_price = self.list_of_sell[i][1]  # 更新成交价格
                                print('agent{}直接买单成交，成交价格{}'.format(self.list_of_buy[0][2],self.now_price))
                            else:
                                self.list_of_buy[0][0] += self.list_of_sell[i][0]  # 更新买单量
                                self.list_of_sell[i][0]=0 #清卖单
                                self.now_price = self.list_of_sell[i][1]
                                print('agent{}卖单全部分成交，成交价为{}'.format(self.list_of_sell[i][2], self.now_price))
                                print('agent{}买单部分成交，成交价为{}'.format(self.list_of_buy[0][2],self.now_price))

                        i+=1

        return self.now_price, self.list_of_sell, self.list_of_buy #返回当前价格，挂单信息
    def _update_list(self,list_of_sell,list_of_buy): # 更新买单卖单
        self.list_of_sell, self.list_of_buy = list_of_sell,list_of_buy #


    def market_price(self): #返回市价
        return self.now_price

    def reset(self):
        # initiate state
        self.state = self._initiate_state()


        return self.state

    def render(self, mode="human", close=False):
        return self.state

    def _initiate_state(self):

        pass



    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def get_sb_env(self):
        e = DummyVecEnv([lambda: self])
        obs = e.reset()
        return e, obs
