# crystal_db.py
# 真实水晶库存数据库 - 2025 优化版 (已删除绿檀，包含老山檀)

CRYSTAL_INVENTORY = {
    "木": [
        {"name": "羽毛萤石", "desc": "充满灵性，提升直觉与治愈", "color": "绿色"},
        {"name": "绿锂辉", "desc": "畅通七轮，招财助运", "color": "浅绿"},
        {"name": "蓝绿晶", "desc": "对应喉轮，增强表达能力", "color": "蓝绿"},
        {"name": "绿阿塞", "desc": "高频能量，强力疗愈与清理", "color": "深绿"},
        {"name": "葡萄石", "desc": "希望之石，指引方向，招正财", "color": "淡绿"},
        # 绿檀 已删除
        {"name": "沉香", "desc": "纯阳之气，净化磁场", "color": "深褐"},
        {"name": "老山檀", "desc": "檀香之王，醇厚奶香，定心安神，招正财", "color": "深褐"},
        {"name": "绿发晶", "desc": "正财聚财，事业顺利", "color": "绿色"},
        {"name": "绿纹石", "desc": "释放焦虑，带来愉悦", "color": "翠绿"},
        {"name": "和田玉", "desc": "温润养人，平安吉祥", "color": "青白"}
    ],
    "火": [
        {"name": "紫锂辉", "desc": "梦幻之石，缓解压力", "color": "淡紫"},
        {"name": "粉晶", "desc": "招桃花，改善人际关系", "color": "粉色"},
        {"name": "紫牙乌", "desc": "美容养颜，增强气血", "color": "深红"},
        {"name": "磷灰石", "desc": "激发积极性，消除冷漠", "color": "紫蓝"},
        {"name": "红胶花", "desc": "开运招财，贵人相助", "color": "红色"},
        {"name": "紫水晶", "desc": "开发智慧，学业有成，提升专注", "color": "紫色"},
        {"name": "红纹石", "desc": "爱神之石，吸引真爱，求姻缘", "color": "玫瑰红"},
        {"name": "南红", "desc": "养心养血，佛教七宝", "color": "赤红"},
        {"name": "朱砂", "desc": "极阳之物，镇煞辟邪，保平安", "color": "朱红"}
    ],
    "土": [
        {"name": "茶晶", "desc": "稳健踏实，过滤病气", "color": "茶色"},
        {"name": "花珀", "desc": "安神定惊，美容护肤", "color": "金珀色"},
        {"name": "利比亚陨石", "desc": "强大能量，提升灵性", "color": "淡黄"},
        {"name": "柠檬晶", "desc": "主财运，心情开朗", "color": "柠檬黄"},
        {"name": "板钛/钛晶", "desc": "水晶之王，招大财，正偏财", "color": "钛金"},
        {"name": "金虎眼", "desc": "激发勇气，坚定信念", "color": "金褐"},
        {"name": "黑银钛", "desc": "强力避邪，防小人", "color": "黑银"},
        {"name": "奶茶月光", "desc": "温柔气质，舒缓情绪", "color": "米色"},
        {"name": "黄水晶", "desc": "聚财之石，增强自信", "color": "黄色"},
        {"name": "黄塔晶", "desc": "步步高升，事业有成", "color": "黄白"},
        {"name": "黑金超七", "desc": "全能水晶，放大能量", "color": "黑金"},
        {"name": "蜜蜡", "desc": "中医五宝，安神助眠", "color": "蜜黄"},
        {"name": "小树胶花", "desc": "异象水晶，招财纳福", "color": "黄红"}
    ],
    "金": [
        {"name": "白月光", "desc": "恋人之石，柔和光晕，助睡眠", "color": "乳白"},
        {"name": "白雪花幽灵", "desc": "净化心灵，清洗负能", "color": "雪白"},
        {"name": "白幽灵", "desc": "提神醒脑，净化磁场", "color": "透明白"},
        {"name": "白兔毛", "desc": "温和能量，护身保平安", "color": "丝白"},
        {"name": "白水晶", "desc": "水晶之王，平衡身心，学业", "color": "透明"},
        {"name": "象牙果/砗磲", "desc": "佛教圣物，吉祥如意", "color": "象牙白"},
        {"name": "金锂云母", "desc": "招财进宝，贵气逼人，缓解焦虑", "color": "金紫"}
    ],
    "水": [
        {"name": "海蓝宝", "desc": "对应喉轮，加强沟通，口才", "color": "天蓝"},
        {"name": "黑骨干", "desc": "强力落地，排除病气", "color": "灰黑"},
        {"name": "蓝晶石", "desc": "软化固执，清理负能", "color": "深蓝"},
        {"name": "银曜石", "desc": "增强决断，辟邪挡煞，职场", "color": "银黑"},
        {"name": "鹰眼石", "desc": "洞察力，激发勇气", "color": "蓝黑"},
        {"name": "蓝磷灰", "desc": "缓解悲伤，激发灵感", "color": "海蓝"},
        {"name": "蓝虎眼", "desc": "冷静头脑，清晰思路，学业", "color": "深蓝"},
        {"name": "蓝纹玛瑙", "desc": "平复怒气，消除疲劳", "color": "淡蓝"},
        {"name": "拉长石", "desc": "灵魂伴侣，提升魅力，招桃花", "color": "灰蓝"},
        {"name": "彼得石", "desc": "暴风雨宝石，王者之气", "color": "蓝褐"},
        {"name": "黑发晶", "desc": "领袖之石，消除业障，防小人", "color": "黑色"},
        {"name": "蓝线石", "desc": "培养耐心，提升毅力", "color": "蓝紫"}
    ]
}

def get_smart_recommendations(needed_elements, user_colors=[], goal_keywords=[]):
    """智能推荐算法"""
    recommendations = {}
    
    for element in needed_elements:
        if element in CRYSTAL_INVENTORY:
            candidates = []
            for stone in CRYSTAL_INVENTORY[element]:
                score = 0
                stone_copy = stone.copy() 
                
                # 愿望匹配
                for kw in goal_keywords:
                    if kw in stone['desc']:
                        score += 2
                        stone_copy['tag'] = "🎯 愿望匹配"
                
                # 颜色匹配
                for color in user_colors:
                    if color in stone['color'] or color in stone['name']:
                        score += 1
                        if 'tag' not in stone_copy: stone_copy['tag'] = "🎨 颜色匹配"
                
                stone_copy['score'] = score
                candidates.append(stone_copy)
            
            # 排序
            candidates.sort(key=lambda x: x['score'], reverse=True)
            recommendations[element] = candidates
            
    return recommendations