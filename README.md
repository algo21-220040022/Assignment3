# hurst_strategy
In this project, I utilize the "Hurst" strategy highlighted in the reference for bitcoin trading. This "Hurst" strategy construct series of hurst index based on historical price data, and use this index to measure the trend duration. That is, if the index value is high, it suggest that the current trend of price would continue in the recent future; while the index value is low, the current trend of price may be interrupted. So the basic idea is to long the bitcoin when both the index value is high and the current trend is positive, and short the bitcoin when the index value is low

## download_data.py
This file is used to download the daily data from CCXT package.

## main.py
This .py construct the "Hurst" calculation function and simulate the strategy.

## Backtest result
![image](https://github.com/algo21-220040022/hurst_strategy/blob/main/result/backtest_reuslt.png)
