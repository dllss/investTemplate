# -*- coding: utf-8 -*-
import akshare as ak
import pandas as pd

# 获取分众传媒基本信息
print('=' * 50)
print('分众传媒(002027)基础数据获取')
print('=' * 50)

# 1. 股票基本信息
info = ak.stock_individual_info_em(symbol='002027')
print('\n--- 基本信息 ---')
for idx, row in info.iterrows():
    print(f"{row['item']}: {row['value']}")

# 2. 最新股价
df_price = ak.stock_zh_a_spot_em()
df_price = df_price[df_price['代码'] == '002027']
if not df_price.empty:
    print('\n--- 最新股价 ---')
    row = df_price.iloc[0]
    print(f"最新价: {row['最新价']}")
    print(f"总市值: {row['总市值']}")
    print(f"流通市值: {row['流通市值']}")
    print(f"市盈率-动态: {row['市盈率-动态']}")
    print(f"市净率: {row['市净率']}")
    print(f"52周最高: {row['最高']}")
    print(f"52周最低: {row['最低']}")
    print(f"成交额: {row['成交额']}")
    print(f"成交量: {row['成交量']}")

# 3. 财务报表 - 主要指标
print('\n--- 主要财务指标(年报) ---')
try:
    fin = ak.stock_financial_analysis_indicator(symbol='002027')
    print(fin.head(5).to_string())
except Exception as e:
    print(f"财务指标获取失败: {e}")

# 4. 资产负债表
print('\n--- 资产负债表(最近5年) ---')
try:
    bal = ak.stock_balance_sheet_by_report_em(symbol='002027')
    # 获取关键字段
    key_cols = ['REPORT_DATE', 'TOTAL_ASSETS', 'TOTAL_LIABILITIES', 'TOTAL_EQUITY', 
                'MONETARY_FUNDS', 'TRADE_FINANCIAL_ASSETS', 'NOTES_RECEIVABLE', 
                'ACCOUNTS_RECEIVABLE', 'SHORT_TERM_LOAN', 'NON_CURRENT_LIABILITIES']
    bal_filtered = bal[key_cols].head(5) if all(c in bal.columns for c in key_cols) else bal.head(5)
    print(bal_filtered.to_string())
except Exception as e:
    print(f"资产负债表获取失败: {e}")

# 5. 利润表
print('\n--- 利润表(最近5年) ---')
try:
    inc = ak.stock_profit_sheet_by_report_em(symbol='002027')
    key_cols = ['REPORT_DATE', 'TOTAL_OPERATE_INCOME', 'OPERATE_INCOME', 
                'TOTAL_OPERATE_COST', 'OPERATE_COST', 'OPERATE_PROFIT', 
                'NETPROFIT', 'PARENT_NETPROFIT']
    inc_filtered = inc[key_cols].head(5) if all(c in inc.columns for c in key_cols) else inc.head(5)
    print(inc_filtered.to_string())
except Exception as e:
    print(f"利润表获取失败: {e}")

# 6. 现金流量表
print('\n--- 现金流量表(最近5年) ---')
try:
    cash = ak.stock_cash_flow_sheet_by_report_em(symbol='002027')
    key_cols = ['REPORT_DATE', 'SALES_SERVICES', 'NET_OPERATE_CASH_FLOW',
                'PURCHASE_ASSETS', 'NET_INVEST_CASH_FLOW', 'NET_FINANCE_CASH_FLOW']
    cash_filtered = cash[key_cols].head(5) if all(c in cash.columns for c in key_cols) else cash.head(5)
    print(cash_filtered.to_string())
except Exception as e:
    print(f"现金流量表获取失败: {e}")

print('\n' + '=' * 50)
print('数据获取完成')
