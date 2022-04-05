# stock_env
stock environment for reinforcement learning 

定义单只股票的市场交易环境，初始值：<br>
1.流通股本：tradable_shares<br>
2.初始价格：initial_price<br>
3.涨跌停设置：price_limiting <br>
4.交易费率：buy_cost_pct，sell_cost_pct<br>
5.状态空间：state_space<br>
6.动作空间：action_space<br>

状态：
1.流通股本：tradable_shares 【标量】<br> 
2.实时价格：now_price 【标量】<br> 
3.前一日价格:pre_close 【标量】<br> 
4.日订单列表买:list_of_buy  【向量】<br> 
5.日订单列表卖:list_of_sell  【维向量】<br> 
