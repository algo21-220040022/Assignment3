import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from empyrical import max_drawdown

def Hurst(data):
    n = 6
    data = pd.Series(data).pct_change()[1:]
    ARS = list()
    lag = list()
    for i in range(n):
        m = 2 ** i
        size = np.size(data) // m
        lag.append(size)
        panel = {}
        for j in range(m):
            panel[str(j)] = data[j*size:(j+1)*size].values

        panel = pd.DataFrame(panel)
        mean = panel.mean()
        Deviation = (panel - mean).cumsum()
        maxi = Deviation.max()
        mini = Deviation.min()
        sigma = panel.std()
        RS = maxi - mini
        RS = RS / sigma
        ARS.append(RS.mean())
    lag = np.log10(lag)
    ARS = np.log10(ARS)
    hurst_exponent = np.polyfit(lag, ARS, 1)
    hurst = hurst_exponent[0]
    return hurst


data = pd.read_pickle("./data/BTC_daily.pkl")
data.index = pd.to_datetime(data.index)
data.sort_index(ascending=True, inplace=True)
calculate_period = 230
hurst_list = []
close = data["close"].tolist()
date_list = list(data.index[calculate_period:])
target_close = close[calculate_period:]
for i,date in enumerate(date_list):
    if i % 20 == 0:
        print(f"{date}...")
    close_period = close[i:i+calculate_period]
    hurst_list.append(Hurst(close_period))

"""calculate 20 days moving average"""
hurst_ave_list = []
btc_MA20 = []
move_ave = 20 ##hurst指数移动平均天数
btc_move = 20
for i in range(len(hurst_list[50 - 1:])):
    hurst_ave_list.append(sum(hurst_list[i : i + move_ave]) / move_ave)
    btc_MA20.append(sum(target_close[i : i + btc_move]) / btc_move)
date_list20 = date_list[50-1:]

"""calculate 60 days moving average"""
hurst_ave_list60 = []
move_ave = 50 ##hurst指数移动平均天数
for i in range(len(hurst_list[move_ave - 1:])):
    hurst_ave_list60.append(sum(hurst_list[i : i + move_ave]) / move_ave)
date_list60 = date_list[move_ave:]
target_close = target_close[move_ave:]
ret_list = []
base_ret_list = [0]
bought = False
last_price = 0
for i, price in enumerate(target_close):
    if i != 0:
        base_ret_list.append(target_close[i]/target_close[i-1]-1)
    if bought == True:
        ret_list.append(target_close[i]/target_close[i-1]-1)
    else:
        ret_list.append(0)
    if hurst_ave_list[i] >= 0.55 and btc_MA20[i]>0:
        bought = True
    elif hurst_ave_list[i] < 0.55 and hurst_ave_list[i]<hurst_ave_list60:
        bought = False
ret_arr = np.array(ret_list)
base_ret_arr = np.array(base_ret_list)
net_value_arr = (1+ret_arr).cumprod()
base_net_value_arr = (1+base_ret_arr).cumprod()
maxDD = max_drawdown(net_value_arr)
annual_ret = (net_value_arr[-1])**(250/len(net_value_arr[1:]))-1
volatility = np.std(ret_arr[1:])*np.sqrt(250)
sharpe = (annual_ret-0.03)/volatility
print(f"annual return: {annual_ret}\n"
      f"volatility: {volatility}\n"
      f"sharpe: {sharpe}\n"
      f"max drawdown: {maxDD}")
plot_df = pd.DataFrame({"portfolio":net_value_arr, "base":base_net_value_arr}, index=date_list60)
plot_df.plot()
plt.show()

"""Above codes plot the hurst index and BTC close price series"""
plt.rcParams['figure.figsize'] = (25,8)
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.set_xlabel('时间')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  #設置x軸主刻度顯示格式（日期）
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=10))
plt.gcf().autofmt_xdate()
ax1.plot(date_list60[1:], target_close[1:], color = 'darkorange',label = "BTC", linewidth = 4,zorder = 1)
ax1.plot(date_list20[1:], btc_MA20[1:], color = 'g',label = "BTC_MA20", linewidth = 4,zorder = 1)
# ax1.plot(date_list60, target_close, color = 'darkorange',label = "BTC", linewidth = 4,zorder = 1)
ax1.legend(loc=4,  fontsize = 30)
# ax2.plot(date_list60, net_value_arr,color = 'darkturquoise', label = "net_value",linewidth = 3)

ax2.plot(date_list20[1:], hurst_ave_list[:-1],color = 'darkturquoise', label = "Hurst_MA20",linewidth = 3)
ax2.plot(date_list60, hurst_ave_list60[1:],color = 'b', label = "Hurst_MA60",linewidth = 3)
ax2.plot(date_list20[1:], [0.55 for i in range(len(date_list20[1:]))], color = 'r')
ax2.legend(loc=0,  fontsize = 30)
plt.show()
