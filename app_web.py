# app_web.py
# 2025 品牌运营最终版：移除颜色偏好选择
import streamlit as st
import os
import datetime
import importlib
import pandas as pd
import random
import string
from lunar_python import Lunar
from PIL import Image

# 强制加载核心模块
import calc_bazi
importlib.reload(calc_bazi)
from calc_bazi import get_bazi_info, analyze_liunian_strategy

import crystal_db
importlib.reload(crystal_db)
from crystal_db import get_smart_recommendations 

# ===========================
# 🖼️ 品牌素材加载
# ===========================
LOGO_PATH = "logo.jpg" 

logo_img = "💎" 
logo_for_display = None 

if os.path.exists(LOGO_PATH):
    try:
        loaded_img = Image.open(LOGO_PATH)
        logo_img = loaded_img 
        logo_for_display = loaded_img
    except Exception as e:
        print(f"图片加载失败: {e}")
        logo_img = "💎"

# 3. 页面配置
st.set_page_config(
    page_title="一条禾瑜 | 水晶命理高定",
    layout="wide",
    page_icon=logo_img 
)

# ===========================
# 🔐 全局配置
# ===========================
ADMIN_PASSWORD = "888"         
CODES_FILE = "invite_codes.csv" 
HISTORY_FILE = "customer_history.csv"

# ===========================
# 📂 邀请码管理系统
# ===========================
def init_code_db():
    if not os.path.exists(CODES_FILE):
        df = pd.DataFrame(columns=["邀请码", "总次数", "已用次数", "备注", "创建时间"])
        df.to_csv(CODES_FILE, index=False, encoding='utf-8-sig')

def generate_invite_code(limit=5, note="VIP客户"):
    init_code_db()
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    new_data = {"邀请码": code, "总次数": limit, "已用次数": 0, "备注": note, "创建时间": datetime.datetime.now().strftime("%Y-%m-%d")}
    df = pd.read_csv(CODES_FILE)
    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    df.to_csv(CODES_FILE, index=False, encoding='utf-8-sig')
    return code

def verify_and_use_code(code):
    init_code_db()
    if not code: return False, 0, "请输入邀请码"
    try:
        df = pd.read_csv(CODES_FILE)
        mask = df["邀请码"].astype(str) == str(code).strip()
        if not mask.any(): return False, 0, "❌ 无效的邀请码"
        idx = df[mask].index[0]
        total = df.at[idx, "总次数"]
        used = df.at[idx, "已用次数"]
        if used >= total: return False, 0, "⛔ 此邀请码次数已耗尽"
        return True, total - used, "✅ 邀请码有效"
    except: return False, 0, "系统错误"

def deduct_code_count(code):
    df = pd.read_csv(CODES_FILE)
    mask = df["邀请码"].astype(str) == str(code).strip()
    if mask.any():
        idx = df[mask].index[0]
        df.at[idx, "已用次数"] += 1
        df.to_csv(CODES_FILE, index=False, encoding='utf-8-sig')

# ===========================
# 🟢 侧边栏：品牌标识与登录
# ===========================
if logo_for_display:
    st.sidebar.image(logo_for_display, width=150)
    
st.sidebar.markdown("### 一条禾瑜 · 水晶命理")
st.sidebar.caption("专属高定 | 能量平衡 | 运势加持")
st.sidebar.markdown("---")

# 2. 登录验证
st.sidebar.title("💎 登录验证")
auth_mode = st.sidebar.radio("身份", ["👤 贵宾使用", "🔑 店主管理"])

current_code = ""
is_verified = False
remain_times = 0

if auth_mode == "👤 贵宾使用":
    current_code = st.sidebar.text_input("请输入您的邀请码", placeholder="例如: X7Y9Z2")
    if current_code:
        valid, remain, msg = verify_and_use_code(current_code)
        if valid:
            st.sidebar.success(f"认证成功！剩余次数: {remain}")
            is_verified = True
        else:
            st.sidebar.error(msg)
else:
    # 店主模式
    admin_pwd = st.sidebar.text_input("管理员密码", type="password")
    if admin_pwd == ADMIN_PASSWORD:
        st.sidebar.success("🔓 管理员已登录")
        is_verified = True
        st.sidebar.markdown("---")
        st.sidebar.subheader("后台发卡系统")
        with st.sidebar.form("gen_code"):
            new_limit = st.number_input("可用次数", 1, 100, 5)
            new_note = st.text_input("备注 (如: 王总)", "VIP客户")
            if st.form_submit_button("生成新邀请码"):
                new_code = generate_invite_code(new_limit, new_note)
                st.sidebar.code(new_code, language="text")
                st.sidebar.success("已生成！请复制给客人")
        if st.sidebar.checkbox("查看邀请码列表"):
            init_code_db()
            df_codes = pd.read_csv(CODES_FILE)
            st.sidebar.dataframe(df_codes)

st.sidebar.markdown("---")

# ===========================
# 🟢 侧边栏：定制参数 (仅验证通过后显示)
# ===========================
if is_verified:
    st.sidebar.title("💎 定制参数")
    customer_name = st.sidebar.text_input("您的称呼", value="贵宾")
    gender = st.sidebar.selectbox("性别", ["男", "女"])
    birth_date = st.sidebar.date_input("出生日期", value=datetime.date(1995, 11, 1))
    t_c1, t_c2 = st.sidebar.columns(2)
    with t_c1: hour = st.sidebar.number_input("时", 0, 23, 12)
    with t_c2: minute = st.sidebar.number_input("分", 0, 59, 30)
    
    st.sidebar.subheader("核心愿望")
    user_goal = st.sidebar.selectbox("选择愿望", ["📅 年度流年运势", "平衡/综合", "求财/事业", "求姻缘", "求健康"])
    if "流年" in user_goal:
        target_year = st.sidebar.selectbox("年份", [2025, 2026])
    else:
        target_year = 2025

    analysis_mode = st.sidebar.radio("模式", ["🤖 AI 智能", "🧠 专家人工"])
    manual_elements = []
    if analysis_mode == "🧠 专家人工":
        st.sidebar.caption("请勾选推荐五行:")
        m_cols = st.sidebar.columns(5)
        for i, l in enumerate(["金","木","水","火","土"]):
            if m_cols[i].checkbox(l): manual_elements.append(l)
    
    # 【已修改】移除了颜色偏好的UI组件，改为默认空列表
    user_colors = [] 

# ===========================
# 🔵 主界面逻辑
# ===========================
col_logo, col_title = st.columns([1, 6])
with col_logo:
    if logo_for_display:
        st.image(logo_for_display, width=110)
    else:
        st.write("💎")
        
with col_title:
    st.title("一条禾瑜")
    st.markdown("##### 🔮 专属水晶命理高定系统")

st.markdown("---")

if not is_verified:
    st.info("👋 欢迎光临！本系统为**预约邀请制**。")
    st.warning("请在左侧输入 **【邀请码】** 开启您的专属定制服务。")
    st.stop()

if st.button("🚀 开始生成方案 (扣除1次)"):
    
    if analysis_mode == "🧠 专家人工" and not manual_elements:
        st.error("专家模式请至少勾选一个五行")
    else:
        with st.spinner("正在核销权益并生成方案..."):
            # 1. 扣除次数
            if auth_mode == "👤 贵宾使用":
                deduct_code_count(current_code)
            
            # 2. 排盘
            bazi_report = get_bazi_info(birth_date.year, birth_date.month, birth_date.day, hour, minute, gender, "北京")
            analysis = bazi_report['命理分析']
            
            # 3. 确定喜用
            final_elements = []
            final_desc = ""
            if analysis_mode == "🧠 专家人工":
                final_elements = manual_elements
                final_desc = "专家指定方案"
            else:
                if "流年" in user_goal:
                    lunar = Lunar.fromYmd(target_year, 6, 1)
                    final_elements, final_desc, _ = analyze_liunian_strategy(
                        analysis, lunar.getYearGan(), lunar.getYearZhi(), analysis["年支"]
                    )
                else:
                    final_elements = analysis['喜用神']
                    final_desc = analysis['分析文案']

            # 4. 匹配
            kw_map = {"求财":["财"], "姻缘":["桃","爱"], "健康":["安"]}
            goal_kws = []
            for k,v in kw_map.items(): 
                if k in user_goal: goal_kws+=v
            
            # 这里 user_colors 传的是空列表，表示不限颜色
            matched = get_smart_recommendations(final_elements, user_colors, goal_kws)

            # 5. 展示
            st.success("✅ 方案生成成功！")
            
            # 八字区
            with st.container():
                st.subheader(f"📜 {customer_name} 的命盘原局")
                cols = st.columns(4)
                for i, p in enumerate(bazi_report['八字']): cols[i].metric(["年","月","日","时"][i], p)
            
            # 结论区
            st.info(f"💡 命理建议：{final_desc}")
            c1, c2 = st.columns(2)
            c1.metric("格局", analysis['格局'])
            c2.metric("推荐五行", "/".join(final_elements))
            
            st.markdown("---")
            
            # 图片区
            st.subheader("🔮 专属材质推荐")
            if matched:
                for elem, stones in matched.items():
                    st.markdown(f"**【补{elem}】**")
                    icols = st.columns(3)
                    for idx, s in enumerate(stones):
                        with icols[idx%3]:
                            path = f"images_product/{s['name']}.jpg"
                            if not os.path.exists(path): path = f"images/{s['name']}.jpg"
                            if os.path.exists(path): st.image(path, use_container_width=True)
                            st.caption(f"{s['name']}")
                    st.markdown("---")
            else:
                st.warning("暂无匹配材质")

            # 记录历史
            try:
                pd.DataFrame([{
                    "时间": datetime.datetime.now(),
                    "邀请码": current_code if auth_mode=="👤 贵宾使用" else "管理员",
                    "客户": customer_name,
                    "推荐": "/".join(final_elements)
                }]).to_csv(HISTORY_FILE, mode='a', header=not os.path.exists(HISTORY_FILE), index=False, encoding='utf-8-sig')
            except: pass