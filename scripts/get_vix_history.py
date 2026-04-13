#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取历史VIX数据
数据来源：Yahoo Finance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_vix_history(start_date='2000-01-01', end_date=None):
    """
    获取VIX历史数据
    
    参数:
        start_date: 开始日期（格式：YYYY-MM-DD）
        end_date: 结束日期（默认为今天）
    
    返回:
        DataFrame: VIX历史数据
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"📊 正在获取VIX历史数据 ({start_date} 至 {end_date})...")
    
    try:
        # 获取VIX数据（Yahoo Finance代码为^VIX）
        vix = yf.download('^VIX', start=start_date, end=end_date, progress=False)
        
        if vix.empty:
            print("❌ 未获取到数据")
            return None
        
        print(f"✅ 成功获取 {len(vix)} 条数据")
        
        # 数据统计
        print("\n" + "="*60)
        print("📈 VIX历史统计")
        print("="*60)
        print(f"平均值: {vix['Close'].mean():.2f}")
        print(f"最高值: {vix['Close'].max():.2f} (日期: {vix['Close'].idxmax().strftime('%Y-%m-%d')})")
        print(f"最低值: {vix['Close'].min():.2f} (日期: {vix['Close'].idxmin().strftime('%Y-%m-%d')})")
        print(f"当前值: {vix['Close'][-1]:.2f}")
        
        # VIX分档统计
        print("\n" + "="*60)
        print("📊 VIX分档统计（占比）")
        print("="*60)
        total_days = len(vix)
        vix_close = vix['Close']
        
        extreme_panic = (vix_close >= 40).sum()
        panic = ((vix_close >= 30) & (vix_close < 40)).sum()
        anxiety = ((vix_close >= 20) & (vix_close < 30)).sum()
        normal = ((vix_close >= 12) & (vix_close < 20)).sum()
        calm = (vix_close < 12).sum()
        
        print(f"VIX ≥ 40 (极度恐慌):  {extreme_panic:4d}天 ({extreme_panic/total_days*100:5.2f}%)")
        print(f"VIX 30-40 (恐慌):    {panic:4d}天 ({panic/total_days*100:5.2f}%)")
        print(f"VIX 20-30 (焦虑):    {anxiety:4d}天 ({anxiety/total_days*100:5.2f}%)")
        print(f"VIX 12-20 (正常):    {normal:4d}天 ({normal/total_days*100:5.2f}%)")
        print(f"VIX < 12 (平静):     {calm:4d}天 ({calm/total_days*100:5.2f}%)")
        
        # 重大事件标注
        print("\n" + "="*60)
        print("🔥 历史重大恐慌事件（VIX ≥ 40）")
        print("="*60)
        
        extreme_events = vix[vix['Close'] >= 40].sort_values('Close', ascending=False).head(10)
        for idx, row in extreme_events.iterrows():
            date_str = idx.strftime('%Y-%m-%d')
            vix_value = row['Close']
            print(f"{date_str}: VIX = {vix_value:.2f}")
        
        return vix
        
    except Exception as e:
        print(f"❌ 获取数据失败: {e}")
        return None

def plot_vix_history(vix_data, save_path=None):
    """
    绘制VIX历史走势图
    
    参数:
        vix_data: VIX数据DataFrame
        save_path: 图片保存路径（可选）
    """
    if vix_data is None or vix_data.empty:
        print("❌ 无数据可绘制")
        return
    
    print("\n📊 正在绘制VIX历史走势图...")
    
    plt.figure(figsize=(15, 8))
    
    # 绘制VIX走势
    plt.plot(vix_data.index, vix_data['Close'], linewidth=1, color='#2E86C1', label='VIX')
    
    # 添加水平参考线
    plt.axhline(y=40, color='red', linestyle='--', linewidth=1, alpha=0.5, label='极度恐慌(40)')
    plt.axhline(y=30, color='orange', linestyle='--', linewidth=1, alpha=0.5, label='恐慌(30)')
    plt.axhline(y=20, color='yellow', linestyle='--', linewidth=1, alpha=0.5, label='焦虑(20)')
    plt.axhline(y=12, color='green', linestyle='--', linewidth=1, alpha=0.5, label='平静(12)')
    
    # 填充区域
    plt.fill_between(vix_data.index, 0, vix_data['Close'], 
                     where=(vix_data['Close'] >= 40), alpha=0.3, color='red', label='极度恐慌区')
    plt.fill_between(vix_data.index, 0, vix_data['Close'], 
                     where=((vix_data['Close'] >= 30) & (vix_data['Close'] < 40)), 
                     alpha=0.3, color='orange', label='恐慌区')
    
    plt.title('VIX恐慌指数历史走势', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('日期', fontsize=12)
    plt.ylabel('VIX值', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ 图表已保存到: {save_path}")
    
    plt.show()

def save_to_csv(vix_data, output_path='vix_history.csv'):
    """
    保存VIX数据到CSV文件
    
    参数:
        vix_data: VIX数据DataFrame
        output_path: 输出文件路径
    """
    if vix_data is None or vix_data.empty:
        print("❌ 无数据可保存")
        return
    
    try:
        vix_data.to_csv(output_path, encoding='utf-8-sig')
        print(f"\n💾 数据已保存到: {output_path}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")

def analyze_vix_for_strategy(vix_data):
    """
    分析VIX数据，为定投策略提供建议
    
    参数:
        vix_data: VIX数据DataFrame
    """
    if vix_data is None or vix_data.empty:
        return
    
    current_vix = vix_data['Close'][-1]
    avg_vix_1y = vix_data['Close'][-252:].mean()  # 最近1年平均
    avg_vix_5y = vix_data['Close'][-1260:].mean()  # 最近5年平均
    
    print("\n" + "="*60)
    print("💡 VIX定投策略建议")
    print("="*60)
    print(f"当前VIX: {current_vix:.2f}")
    print(f"1年平均: {avg_vix_1y:.2f}")
    print(f"5年平均: {avg_vix_5y:.2f}")
    print()
    
    if current_vix >= 40:
        print("🔥 极度恐慌！建议：加倍定投6,000元")
        print("   历史上VIX≥40只出现过{:.1f}%的时间，属于极佳买点".format(
            ((vix_data['Close'] >= 40).sum() / len(vix_data) * 100)))
    elif current_vix >= 30:
        print("😱 市场恐慌！建议：加倍定投6,000元")
        print("   历史上VIX≥30只出现过{:.1f}%的时间，属于优质买点".format(
            ((vix_data['Close'] >= 30).sum() / len(vix_data) * 100)))
    elif current_vix >= 25:
        print("😟 市场焦虑！建议：加大定投4,500元")
    elif current_vix >= 20:
        print("😐 市场波动！建议：标准定投3,000元")
    elif current_vix >= 15:
        print("🙂 市场平静！建议：暂停定投，持有观察")
    elif current_vix >= 12:
        print("😊 市场乐观！建议：考虑小幅减仓10%")
    else:
        print("😍 市场极度乐观！建议：大幅减仓25%")
        print("   历史上VIX<12只出现过{:.1f}%的时间，通常是获利良机".format(
            ((vix_data['Close'] < 12).sum() / len(vix_data) * 100)))

def main():
    """
    主函数
    """
    print("\n" + "="*60)
    print("📊 VIX历史数据获取工具")
    print("="*60)
    
    # 获取最近5年VIX数据
    start_date = (datetime.now() - timedelta(days=365*5)).strftime('%Y-%m-%d')
    vix_data = get_vix_history(start_date=start_date)
    
    if vix_data is not None:
        # 保存到CSV
        save_to_csv(vix_data, 'vix_history_5years.csv')
        
        # 策略分析
        analyze_vix_for_strategy(vix_data)
        
        # 绘制图表
        plot_vix_history(vix_data, save_path='vix_history_chart.png')
        
        print("\n" + "="*60)
        print("✨ 完成！")
        print("="*60)
        print("📁 生成文件:")
        print("  - vix_history_5years.csv (数据文件)")
        print("  - vix_history_chart.png (走势图)")
        print("="*60)

if __name__ == "__main__":
    # 检查依赖
    try:
        import yfinance
        import matplotlib
    except ImportError as e:
        print("❌ 缺少依赖库，请先安装:")
        print("pip3 install yfinance matplotlib")
        exit(1)
    
    main()
