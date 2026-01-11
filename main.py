import pandas as pd
import math
import os
from PIL import Image, ImageDraw

# === 1. 设置：手串参数 ===
BRACELET_SIZE_CM = 15      # 目标手围 (厘米)
CANVAS_SIZE = (800, 800)   # 图片大小
CENTER = (400, 400)        # 圆心位置

def load_inventory():
    """读取库存数据"""
    path = 'data/inventory.xlsx'
    if not os.path.exists(path):
        print("❌ 错误：找不到库存表，请先运行 init.py")
        return None
    return pd.read_excel(path)

def analyze_bazi(year, month, day, hour):
    """
    这里模拟八字分析逻辑。
    (真实商业版需要接入复杂的万年历算法，这里仅做演示：假设缺'火')
    """
    print(f"正在分析生辰: {year}-{month}-{day} {hour}时...")
    # 模拟结果：五行缺火，喜用神为 火
    return "火"

def select_crystals(needed_element, df_inventory):
    """根据缺的五行，从库存挑选水晶"""
    print(f"🎯 客户五行缺 [{needed_element}]，正在筛选库存...")
    
    # 1. 找主珠 (对应五行的)
    main_candidates = df_inventory[
        (df_inventory['五行'] == needed_element) & 
        (df_inventory['类型'] == '主珠')
    ]
    
    # 2. 找配珠 (如果没有同属性的，就用全能的白水晶/金)
    side_candidates = df_inventory[df_inventory['五行'] == '金'] 
    
    design_plan = []
    
    # 如果仓库里有货，就选第一种；没货就用默认的
    if not main_candidates.empty:
        main_bead = main_candidates.iloc[0]
    else:
        print(f"⚠️ 仓库里没有五行属[{needed_element}]的主珠，使用默认方案。")
        main_bead = df_inventory.iloc[0] # 随便拿一个
        
    if not side_candidates.empty:
        side_bead = side_candidates.iloc[0]
    else:
        side_bead = df_inventory.iloc[-1]

    # --- 简单的排列逻辑 ---
    # 逻辑：1颗主珠 + N颗配珠
    # 计算需要多少颗配珠： (手围 - 主珠大小) / 配珠大小
    main_size_cm = main_bead['尺寸mm'] / 10
    side_size_cm = side_bead['尺寸mm'] / 10
    
    remaining_len = BRACELET_SIZE_CM - main_size_cm
    num_side_beads = int(remaining_len / side_size_cm)
    
    print(f"✅ 设计生成：1颗 {main_bead['名称']} + {num_side_beads}颗 {side_bead['名称']}")

    # 加入列表
    # 格式：{'image': 文件名, 'size': 毫米数}
    design_plan.append({'image': main_bead['图片文件名'], 'size': main_bead['尺寸mm']})
    for _ in range(num_side_beads):
        design_plan.append({'image': side_bead['图片文件名'], 'size': side_bead['尺寸mm']})
        
    return design_plan

def generate_preview(design_plan):
    """画图函数"""
    print("🎨 正在绘制预览图...")
    
    # 创建白色背景画布
    canvas = Image.new("RGBA", CANVAS_SIZE, (255, 255, 255, 255))
    
    # 计算半径
    total_mm = sum([b['size'] for b in design_plan])
    radius = (total_mm * 1.5) # 稍微放大一点半径
    
    num_beads = len(design_plan)
    angle_step = 360 / num_beads
    
    for i, bead in enumerate(design_plan):
        # 计算坐标
        angle_rad = math.radians(i * angle_step - 90) # -90度是为了让第一颗在正上方
        x = CENTER[0] + radius * math.cos(angle_rad)
        y = CENTER[1] + radius * math.sin(angle_rad)
        
        # 读取图片
        img_path = f"images/{bead['image']}"
        try:
            bead_img = Image.open(img_path).convert("RGBA")
            
            # 缩放图片 (像素 = mm * 8) 
            pixel_size = int(bead['size'] * 8)
            bead_img = bead_img.resize((pixel_size, pixel_size))
            
            # 粘贴 (注意要减去图片一半大小，让中心对齐)
            paste_x = int(x - pixel_size/2)
            paste_y = int(y - pixel_size/2)
            
            # 第三个参数 bead_img 是用来做透明遮罩的，去掉背景
            canvas.paste(bead_img, (paste_x, paste_y), bead_img)
            
        except FileNotFoundError:
            print(f"❌ 警告：找不到图片 {img_path}，跳过绘制。")
            # 画个圆圈代替
            draw = ImageDraw.Draw(canvas)
            draw.ellipse([x-20, y-20, x+20, y+20], fill='gray')

    # 保存
    canvas.show() # 自动打开图片
    canvas.save("result_design.png")
    print("✨ 设计图已保存为 result_design.png")

# === 主程序入口 ===
if __name__ == "__main__":
    # 1. 读取库存
    df = load_inventory()
    
    if df is not None:
        # 2. 假设输入客户生日 (这里先写死，后面可以改成手动输入)
        needed_element = analyze_bazi(1995, 5, 20, 10)
        
        # 3. 选珠子
        plan = select_crystals(needed_element, df)
        
        # 4. 画图
        generate_preview(plan)