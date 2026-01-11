# app_system.py
import sys
import time
from calc_bazi import get_bazi_info 
from crystal_db import get_crystals_by_elements
# 导入新的绘图函数
from design_gen import generate_full_report_design 

def get_user_input():
    print("\n请录入客户信息 (输入后按回车):")
    try:
        gender = input("   1. 性别 (男/女): ").strip()
        place = input("   2. 出生地 (例如 北京): ").strip()
        
        print("   --- 出生时间 (公历) ---")
        year = int(input("   3. 年份 (例如 1995): "))
        month = int(input("   4. 月份 (1-12): "))
        day = int(input("   5. 日期 (1-31): "))
        hour = int(input("   6. 小时 (0-23): "))
        
        return year, month, day, hour, gender, place
    except ValueError:
        print("⚠️ 格式错误，时间必须是数字！")
        return None

def main():
    print("\n" + "="*50)
    print("🔮  智能八字配饰定制系统 v4.0 (高定版)  🔮")
    print("="*50)
    
    # 1. 获取输入
    data = get_user_input()
    if not data: return
    year, month, day, hour, gender, place = data
    
    print(f"\n⏳ 正在排盘: {place}生人 | {gender}命 | {year}-{month}-{day} {hour}时...")
    time.sleep(1)
    
    # 2. 八字计算 (传入性别和地点)
    bazi_report = get_bazi_info(year, month, day, hour, gender, place)
    analysis = bazi_report['命理分析']
    needed_elements = analysis['喜用神']
    
    # 3. 终端打印简报
    print("\n" + "-"*50)
    print(f"📜 八字乾坤: {'  '.join(bazi_report['八字'])}")
    print(f"💡 命局诊断: {analysis['分析文案']}")
    print(f"🍀 喜用五行: {needed_elements}")
    print("-" * 50)
    
    # 4. 库存匹配
    print("🔍 正在匹配库存...")
    matched_crystals = get_crystals_by_elements(needed_elements)
    
    if matched_crystals:
        for elem, stones in matched_crystals.items():
            print(f"   [{elem}]系可用: " + ", ".join([s['name'] for s in stones]))
    else:
        print("⚠️ 库存不足，无法匹配。")

    # 5. 生成终极设计图
    print("\n🎨 正在绘制八字排盘设计稿...")
    # 注意：这里我们把整个 bazi_report 都传进去了，因为图上要写八字
    generate_full_report_design(bazi_report, matched_crystals)
    
    print("\n" + "="*50)
    input("🎉 程序运行结束。请查看 result_bazi_design.png，按回车退出...")

if __name__ == "__main__":
    main()