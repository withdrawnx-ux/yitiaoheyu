import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

def load_bead_texture(name, size):
    """加载图片并处理成带高光的立体圆珠"""
    path = f"images/{name}.jpg"
    if os.path.exists(path):
        img = Image.open(path).convert("RGB")
    else:
        # 如果没图，生成一个对应五行颜色的占位球
        img = Image.new("RGB", (size, size), (200, 200, 200))
    
    img = ImageOps.fit(img, (size, size), method=Image.Resampling.LANCZOS)
    
    # 圆形遮罩
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse((2, 2, size-2, size-2), fill=255)
    
    # 模拟表面高光
    overlay = Image.new('RGBA', (size, size), (0,0,0,0))
    ImageDraw.Draw(overlay).ellipse((size//4, size//4, size//2, size//2), fill=(255, 255, 255, 120))
    img.paste(overlay, (0, 0), overlay)
    
    return img, mask

def generate_full_report_design(bazi_data, matched_crystals, customer_id, wrist_size, bead_size):
    """生成包含八字排盘和手串的设计图"""
    W, H = 1000, 1100
    image = Image.new("RGB", (W, H), (252, 250, 245))
    draw = ImageDraw.Draw(image)

    # 1. 字体配置
    try:
        font_main = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 28)
        font_title = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 45)
        font_bazi = ImageFont.truetype("C:/Windows/Fonts/simkai.ttf", 40)
    except:
        font_main = font_title = font_bazi = ImageFont.load_default()

    # 2. 绘制顶部八字信息
    draw.text((W//2, 60), "水晶命理定制报告", font=font_title, fill=(50, 50, 50), anchor="mm")
    draw.line((100, 120, 900, 120), fill=(200, 200, 200), width=2)
    
    # 排盘展示
    bazi = bazi_data['八字']
    cols = ["年柱", "月柱", "日柱", "时柱"]
    for i, col_name in enumerate(cols):
        x = 200 + i * 200
        draw.text((x, 160), col_name, font=font_main, fill=(100, 100, 100), anchor="mm")
        draw.text((x, 210), bazi[i], font=font_bazi, fill=(180, 50, 50), anchor="mm")

    # 3. 手串物理排列计算
    # 颗数 = 手围*10 / 珠径
    num_beads = int((wrist_size * 10) / (bead_size * 0.95)) 
    center_x, center_y = W // 2, H // 2 + 150
    radius = 240 # 手串圆环半径
    bead_px = int(bead_size * 4.5) # 珠子像素大小

    # 4. 绘制穿绳背景环
    draw.ellipse((center_x-radius, center_y-radius, center_x+radius, center_y+radius), outline=(230, 220, 210), width=3)

    # 5. 绘制珠子
    elements = list(matched_crystals.keys())
    for i in range(num_beads):
        angle = (2 * math.pi / num_beads) * i - math.pi/2
        cx = center_x + radius * math.cos(angle)
        cy = center_y + radius * math.sin(angle)
        
        # 阴影层
        draw.ellipse((cx-bead_px//2+5, cy-bead_px//2+5, cx+bead_px//2+5, cy+bead_px//2+5), fill=(0,0,0,20))
        
        # 获取对应材质
        elem = elements[i % len(elements)]
        stone_name = matched_crystals[elem][0]['name']
        
        texture, mask = load_bead_texture(stone_name, bead_px)
        image.paste(texture, (int(cx - bead_px//2), int(cy - bead_px//2)), mask)

    # 6. 底部规格标注
    footer_text = f"客户编号: {customer_id}  |  规格: {bead_size}mm / {num_beads}颗  |  设计建议: {bazi_data['命理分析']['喜用神']}"
    draw.text((W//2, H - 80), footer_text, font=font_main, fill=(120, 120, 120), anchor="mm")

    image.save("result_bazi_design.png")