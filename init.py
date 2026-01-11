import pandas as pd
import os

# 1. 确保文件夹存在
os.makedirs('data', exist_ok=True)
os.makedirs('images', exist_ok=True)

# 2. 创建一个标准的库存模板
data = {
    'ID': ['A001', 'A002', 'B001', 'C001'],
    '名称': ['紫水晶', '黄水晶', '红玛瑙', '白水晶'],
    '五行': ['火', '土', '火', '金'],
    '类型': ['主珠', '主珠', '配珠', '隔珠'],
    '库存': [50, 50, 200, 500],
    '尺寸mm': [10, 10, 8, 6],
    '图片文件名': ['amethyst.png', 'citrine.png', 'red_agate.png', 'white.png'],
    '价格': [25.0, 30.0, 5.0, 2.0]
}

df = pd.DataFrame(data)

# 3. 保存为 Excel
file_path = 'data/inventory.xlsx'
try:
    df.to_excel(file_path, index=False)
    print("\n" + "="*40)
    print(f"✅ 成功！库存表已生成：{file_path}")
    print("请去 data 文件夹里看看有没有这个 Excel 文件。")
    print("="*40 + "\n")
except Exception as e:
    print(f"❌ 出错了: {e}")