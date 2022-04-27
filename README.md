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
3.日订单列表买:list_of_buy  【向量】<br> 
4.日订单列表卖:list_of_sell  【维向量】<br> 

--------------------------------------------------------

初始价格10元，通过agent模拟市场交易

![100agent-10ep—balance](https://user-images.githubusercontent.com/63079631/165524424-a74315cd-46cd-4e1c-9f18-99a9ce825ef8.png)
![100agent-10ep—buy](https://user-images.githubusercontent.com/63079631/165524504-f97746ef-a109-4b5a-994c-56352276f4f7.png)
![100agent-10ep—sell](https://user-images.githubusercontent.com/63079631/165524539-a73232fd-b428-4913-bb7b-9f2255ca727c.png)

