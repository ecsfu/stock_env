from agent import agent
from trade_env import StockTradingEnv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

if __name__=='__main__':
    """
    流通股本1亿，初始价格10元
    100个agent,每个agent 20万现金，100万股
    """
    agent_count = 100
    ep = 1
    env = StockTradingEnv(1e9,10,0.1,0.01,0.01,6,4)
    agent_list = []

    price_l=[]
    for i in range(agent_count):
        agent_list.append(agent(i,2e5,1e6)) #初始化100个agent
    for t in range(ep): #假设进行100次交易
        print('*'*70)
        print('第{}次交易循环'.format(t))
        print('*' * 70)
        for i in range(100): #每次交易每个agent各自进行操作
            now_price = env.market_price()
            action = agent_list[i].trade(now_price)
            if action==None:
                print('agent{}持仓不动'.format(agent_list[i].id))
                continue
            print('agent{}执行交易,买/卖{}手，挂单价格为{:.2f}'.format(action[2], action[0], action[1]))
            now_price, list_of_sell, list_of_buy=env.step(action)
            if now_price==None:
                continue
            k=0
            del_sell=[]
            del_buy = []
            for sell,buy in zip(list_of_sell,list_of_buy):
                if sell[0]==0:
                    agent_id = int(sell[2])
                    agent_list[agent_id].update(sell[3]) #更新agent状态
                    del_sell.append(k)

                if buy[0]==0:
                    agent_id = int(buy[2])
                    agent_list[agent_id].update(buy[3]) #更新agent状态
                    del_buy.append(k)

                k+=1
            list_of_sell = np.delete(list_of_sell, del_sell, axis=0)
            list_of_buy = np.delete(list_of_buy,del_buy, axis=0)  # 删除买单
            env._update_list(list_of_sell,list_of_buy)

            print('{}市场价格为{:.2f}'.format(datetime.now().strftime('%H:%M:%S'),now_price))

            price_l.append(now_price)
            index_ = list(range(len(price_l)))

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.plot(index_,price_l)
    plt.xlabel("序列")
    plt.ylabel("价格")
    plt.title('买卖均势')
    plt.show()
    plt.savefig('{}agent-{}ep—balance.png'.format(agent_count,ep))
