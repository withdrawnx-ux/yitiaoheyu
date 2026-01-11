# calc_bazi.py
# 2025 商业旗舰版：八字排盘 + 流年运势 + 太岁检测 + 智能风控
from lunar_python import Solar, Lunar

# --- 基础配置 ---
GAN_WUXING = {"甲":"木", "乙":"木", "丙":"火", "丁":"火", "戊":"土", "己":"土", "庚":"金", "辛":"金", "壬":"水", "癸":"水"}
ZHI_WUXING = {"寅":"木", "卯":"木", "巳":"火", "午":"火", "申":"金", "酉":"金", "亥":"水", "子":"水", "辰":"土", "戌":"土", "丑":"土", "未":"土"}

# 生克链条: 金->水->木->火->土->金
SHENG_MAP = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
KE_MAP = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

def get_wuxing_from_gan(gan): return GAN_WUXING.get(gan, "")
def get_zhi_wuxing(zhi): return ZHI_WUXING.get(zhi, "")

# --- 核心：太岁关系表 (冲、害、刑) ---
def check_tai_sui(user_zhi, year_zhi):
    """
    检查地支由于流年产生的冲克关系
    user_zhi: 用户年支(生肖)
    year_zhi: 流年地支
    """
    # 六冲 (最严重)
    LIU_CHONG = {
        "子":"午", "午":"子", "丑":"未", "未":"丑",
        "寅":"申", "申":"寅", "卯":"酉", "酉":"卯",
        "辰":"戌", "戌":"辰", "巳":"亥", "亥":"巳"
    }
    # 六害 (穿小鞋)
    LIU_HAI = {
        "子":"未", "未":"子", "丑":"午", "午":"丑",
        "寅":"巳", "巳":"寅", "卯":"辰", "辰":"卯",
        "申":"亥", "亥":"申", "酉":"戌", "戌":"酉"
    }
    
    warnings = []
    is_fan_tai_sui = False
    
    if user_zhi == year_zhi:
        warnings.append(f"🔴 **值太岁 (本命年)**：生肖{user_zhi}与流年相同，运势起伏，宜静不宜动。")
        is_fan_tai_sui = True
    elif LIU_CHONG.get(user_zhi) == year_zhi:
        warnings.append(f"💥 **冲太岁**：生肖{user_zhi}与流年{year_zhi}相冲，变动大，易有冲击。")
        is_fan_tai_sui = True
    elif LIU_HAI.get(user_zhi) == year_zhi:
        warnings.append(f"🔪 **害太岁**：生肖{user_zhi}与流年{year_zhi}相害，防小人暗算。")
        is_fan_tai_sui = True
        
    # 刑太岁逻辑 (简化版：寅巳申三刑)
    if (user_zhi == "寅" and year_zhi == "巳") or (user_zhi == "巳" and year_zhi == "申") or (user_zhi == "申" and year_zhi == "寅"):
        warnings.append(f"🔗 **刑太岁**：生肖{user_zhi}与流年{year_zhi}相刑，易有纠纷。")
        is_fan_tai_sui = True
        
    return is_fan_tai_sui, warnings

def analyze_bazi_structure(lunar, wuxing_counts):
    """基础命局分析"""
    day_gan = lunar.getDayGan() 
    month_zhi = lunar.getMonthZhi()
    me = get_wuxing_from_gan(day_gan) 
    month_element = get_zhi_wuxing(month_zhi)
    
    # 找印星
    yin = [k for k,v in SHENG_MAP.items() if v == me][0] 
    
    score_support = wuxing_counts.get(me, 0) + wuxing_counts.get(yin, 0)
    total_score = sum(wuxing_counts.values())
    score_drain = total_score - score_support
    is_strong = score_support >= score_drain
    
    # 风险检测
    risk_flags = []
    need_manual = False
    if abs(score_support - score_drain) <= 2:
        risk_flags.append("⚠️ 能量胶着 (同党异党势均力敌)")
        need_manual = True
    is_month_support = (month_element == me or month_element == yin)
    if is_strong and not is_month_support:
        risk_flags.append("⚠️ 失令反强 (月令不帮扶，却判了身旺)")
        need_manual = True
    elif not is_strong and is_month_support:
        risk_flags.append("⚠️ 得令反弱 (月令帮扶，却判了身弱)")
        need_manual = True
    zeros = list(wuxing_counts.values()).count(0)
    if zeros >= 2:
        risk_flags.append("⚠️ 五行偏枯 (疑似特殊格局)")
        need_manual = True

    if is_strong:
        status = "身旺"
        xi_yong = [v for k,v in SHENG_MAP.items() if k == me] + [v for k,v in KE_MAP.items() if k == me] + [k for k,v in KE_MAP.items() if v == me]
        desc = f"日主[{me}]得势身旺，喜克泄耗。"
    else:
        status = "身弱"
        xi_yong = [me, yin]
        desc = f"日主[{me}]失势身弱，喜生扶。"

    return {
        "日主": day_gan, "日主五行": me, "格局": status, "喜用神": xi_yong,
        "分析文案": desc, "需人工复核": need_manual, "风险提示": risk_flags
    }

def analyze_liunian_strategy(bazi_analysis, liunian_gan, liunian_zhi, user_year_zhi):
    """流年分析策略"""
    xi_yong = bazi_analysis['喜用神']
    
    ln_gan_elem = GAN_WUXING.get(liunian_gan)
    
    recommend_elements = []
    strategy_desc = ""
    has_risk = False
    
    # 1. 太岁检测
    is_fan, fan_warnings = check_tai_sui(user_year_zhi, liunian_zhi)
    
    # 2. 五行策略
    if ln_gan_elem in xi_yong:
        recommend_elements = [ln_gan_elem]
        sheng_ln = [k for k,v in SHENG_MAP.items() if v == ln_gan_elem][0]
        if sheng_ln in xi_yong: recommend_elements.append(sheng_ln)
        strategy_desc = f"流年天干{ln_gan_elem}为喜用。策略：【助旺】。"
    else:
        bridge = SHENG_MAP[ln_gan_elem] 
        if bridge in xi_yong:
            recommend_elements = [bridge]
            strategy_desc = f"流年天干{ln_gan_elem}为忌。策略：【通关】用{bridge}。"
        else:
            controller = [k for k,v in KE_MAP.items() if v == ln_gan_elem][0]
            recommend_elements = [controller]
            strategy_desc = f"流年天干{ln_gan_elem}为忌。策略：【制衡】用{controller}。"
            has_risk = True 

    # 3. 整合太岁信息
    if is_fan:
        has_risk = True 
        strategy_desc += " 【太岁预警】" + " ".join(fan_warnings)
        if "土" not in recommend_elements: recommend_elements.append("土") # 犯太岁建议加土

    if bazi_analysis['日主'] == liunian_gan: 
        has_risk = True
        strategy_desc += " (注：流年与日主伏吟)"

    return recommend_elements, strategy_desc, has_risk

def get_bazi_info(year, month, day, hour, minute=0, gender="男", place="北京"):
    solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
    lunar = solar.getLunar()
    bazi_list = lunar.getBaZi()
    wu_xing_list = lunar.getBaZiWuXing()
    counts = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    for item in wu_xing_list:
        for char in item:
            if char in counts: counts[char] += 1
    
    analysis = analyze_bazi_structure(lunar, counts)
    analysis["年支"] = lunar.getYearZhi() # 返回生肖
    
    return {
        "用户信息": {
            "性别": gender, "出生地": place,
            "阳历": f"{year}-{month}-{day} {hour}:{minute:02d}",
            "农历": f"{lunar.toString()}",
            "生肖": lunar.getYearShengXiao()
        },
        "八字": bazi_list, "五行": wu_xing_list, "五行统计": counts, "命理分析": analysis
    }