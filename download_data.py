
import ccxt
import pandas as pd
import numpy as np
import datetime

epoch = datetime.datetime.utcfromtimestamp(0)
def unix_time_millis(dt):
    if isinstance(dt, str):
        dt=pd.to_datetime(dt)
    return (dt - epoch).total_seconds() * 1000.0

def utc_to_strftime(utc_timestamp):
    return datetime.datetime.fromtimestamp(utc_timestamp/1000).strftime("%Y-%m-%d %H:%M:%S")
exchange = ccxt.bittrex()
output = pd.DataFrame()
exchange.fetch_trades('BTC/USDT')
for year in range(2015,2022):
    daily_data = exchange.fetch_ohlcv('BTC/USDT', '1d', since=unix_time_millis(f"{year}-01-01"))
    daily_data_df =pd.DataFrame(np.array(daily_data), columns=["date","open","high","low","close","volume"])
    index = daily_data_df["date"].apply(utc_to_strftime)
    daily_data_df.index = [i[:10] for i in index]
    output = pd.concat([output, daily_data_df], axis=0)
output.to_pickle("./data/BTC_daily.pkl")