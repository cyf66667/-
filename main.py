from fastapi import FastAPI
from datetime import datetime
import logging
import json
import os
import random
from fastapi.staticfiles import StaticFiles

# 1. 创建存放日志和数据的文件夹
os.makedirs("logs", exist_ok=True)

# 2. 配置全局日志系统
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/luye_app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("LuYe_API")

app = FastAPI(title="鹿野养成计划 API")

# 模拟 10 名用户的独立数据字典（保留了你原来的 last_updated 字段）
mock_users_data = {
    i: {
        "user_id": i, 
        "nickname": f"玩家_{i:03d}", 
        "health": 100, 
        "hunger": 50,  
        "thirst": 50,
        "actions_today": 0,
        "last_updated": "",  # 保留：用于记录最后一次操作的具体时间
        # ==========================================
        # 【新增代码段 1/3】
        # 核心：初始化历史记录列表，给前端详情弹窗提供数据源
        "history": [] 
        # ==========================================
    }
    for i in range(1, 11)
}

def save_user_data_to_json(user_id: int):
    """将指定用户的最新数据，单独保存到他专属的 JSON 文件中"""
    user_data = mock_users_data.get(user_id)
    if not user_data:
        return
        
    today_str = datetime.now().strftime('%Y%m%d')
    file_path = f"logs/user_{user_id}_{today_str}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

# --- 模拟喂食接口（带具体时间） ---
@app.post("/activity/feed/{user_id}")
def feed(user_id: int):
    user = mock_users_data.get(user_id)
    if not user:
        return {"error": "用户未找到"}
        
    now = datetime.now()
    current_hour = now.hour
    # 获取精确到秒的具体时间格式，例如：2026-03-20 16:15:30
    exact_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # 获取餐名（保持你原来的逻辑）
    if 6 <= current_hour < 10:
        meal_name = "早餐"
        hunger_decrease = random.randint(15, 25) 
    elif 11 <= current_hour < 14:
        meal_name = "午餐"
        hunger_decrease = random.randint(25, 40) 
    elif 17 <= current_hour < 21:
        meal_name = "晚餐"
        hunger_decrease = random.randint(20, 35) 
    else:
        meal_name = "零食/夜宵"
        hunger_decrease = random.randint(2, 10) 

    # 改变数值（保持你原来的变量名和逻辑）
    user["hunger"] -= hunger_decrease
    if user["hunger"] < 0:
        user["hunger"] = 0
        
    user["actions_today"] += 1
    user["last_updated"] = exact_time_str  # 更新字典里的操作时间
    
    # ==========================================
    # 【新增代码段 2/3】
    # 核心：在保存前，将本次动作记入历史列表，供前端点击查看。
    # 我们采用 insert(0, ...) 确保最新的记录在列表最前面。
    # 并且只保留最近 10-15 条记录，防止内存无限增长。
    history_entry = {
        "time": exact_time_str,
        "action": f"喂了{meal_name}",
        "effect": f"饥饿值 -{hunger_decrease}"
    }
    user["history"].insert(0, history_entry)
    user["history"] = user["history"][:15] # 限制历史长度
    # ==========================================

    logger.info(f"[集中日志] 用户 {user['nickname']} 喂了{meal_name}，饥饿值降低 {hunger_decrease}，当前饥饿值: {user['hunger']}")
    save_user_data_to_json(user_id)
    
    return {
        "message": f"喂食成功！鹿野吃了一顿{meal_name}", 
        "decreased_by": hunger_decrease,
        "current_hunger": user["hunger"],
        "timestamp": exact_time_str  # 在返回值中带上具体时间
    }

# --- 模拟喂水接口（带具体时间） ---
@app.post("/activity/water/{user_id}")
def water(user_id: int):
    user = mock_users_data.get(user_id)
    if not user:
        return {"error": "用户未找到"}
        
    now = datetime.now()
    exact_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    
    # 确定水型（保持你原来的逻辑和变量名）
    h = now.hour
    if 7 <= h < 10: drink_type, thirst_decrease = "晨间补水", random.randint(20, 30)
    elif 13 <= h < 17: drink_type, thirst_decrease = "午后解暑", random.randint(15, 25)
    elif 21 <= h <= 23: drink_type, thirst_decrease = "睡前适量", random.randint(5, 10)
    else: drink_type, thirst_decrease = "日常小口", random.randint(8, 15)

    user["thirst"] -= thirst_decrease
    if user["thirst"] < 0:
        user["thirst"] = 0
        
    user["actions_today"] += 1
    user["last_updated"] = exact_time_str  # 更新字典里的操作时间
    
    # ==========================================
    # 【新增代码段 3/3】
    # 核心：同喂食接口，将本次喂水记入历史列表。
    user["history"].insert(0, {
        "time": exact_time_str,
        "action": f"进行了{drink_type}",
        "effect": f"口渴值 -{thirst_decrease}"
    })
    user["history"] = user["history"][:15] # 限制历史长度
    # ==========================================

    logger.info(f"[集中日志] 用户 {user['nickname']} 进行了{drink_type}，口渴值降低 {thirst_decrease}，当前口渴值: {user['thirst']}")
    save_user_data_to_json(user_id)
    
    return {
        "message": f"喂水成功！鹿野进行了{drink_type}", 
        "decreased_by": thirst_decrease,
        "current_thirst": user["thirst"],
        "timestamp": exact_time_str  # 在返回值中带上具体时间
    }

# --- 数据大盘接口（前端网页从这里拉取最新数据） ---
@app.get("/api/dashboard")
def get_dashboard_data():
    # 统计今天有互动的活跃玩家（保持不变）
    active_users = sum(1 for u in mock_users_data.values() if u["actions_today"] > 0)
    
    return {
        "total_users": len(mock_users_data),
        "active_users": active_users,
        # 这里的 users 数据包含了现在的完整的 mock_users_data，也自动包含了 history
        "users": list(mock_users_data.values()) # 把所有玩家的数据变成列表发给前端
    }

app.mount("/dashboard", StaticFiles(directory="statics", html=True), name="statics")