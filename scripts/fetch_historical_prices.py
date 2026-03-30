# -*- coding: utf-8 -*-
"""
获取建仓日（2026-03-26）的历史价格
"""

import yfinance as yf
from datetime import datetime, timedelta

tickers = {
    "1522.HK": "京投交通科技",
    "87001.HK": "汇贤产业信托", 
    "882.HK": "天津发展",
    "3320.HK": "华润医药",
}

print("获取 2026-03-26 历史价格...")
print("-" * 60)

for ticker, name in tickers.items():
    try:
        stock = yf.Ticker(ticker)
        # 获取 2026-03-26 前后的数据
        hist = stock.history(start="2026-03-25", end="2026-03-28", interval="1d")
        
        if hist.empty:
            print(f"{name} ({ticker}): 无数据")
            continue
            
        # 找 2026-03-26 的数据
        target_date = "2026-03-26"
        if target_date in hist.index.strftime('%Y-%m-%d'):
            price = hist.loc[target_date]['Close']
            print(f"{name} ({ticker}): {price:.4f}")
        else:
            # 取最接近的日期
            closest = hist.iloc[0]
            date_str = hist.index[0].strftime('%Y-%m-%d')
            print(f"{name} ({ticker}): {closest['Close']:.4f} (日期: {date_str})")
            
    except Exception as e:
        print(f"{name} ({ticker}): 获取失败 - {e}")

print("-" * 60)
