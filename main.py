from fastapi import FastAPI
from datetime import datetime
import logging
import json
import os
from fastapi.staticfiles import StaticFiles

# 1. 创建存放日志和数据的文件夹
os.makedirs("logs", exist_ok=True)

# 2. 配置全局日志系统（所有用户的操作都会记录在这里）
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

# 模拟 10 名用户的独立数据字典（使用 user_id 作为键，方便快速查找）
mock_users_data = {
    i: {
        "user_id": i, 
        "nickname": f"玩家_{i:03d}", 
        "health": 100, 
        "hunger": 0, 
        "actions_today": 0
    }
    for i in range(1, 11)
}

def save_user_data_to_json(user_id: int):
    """将指定用户的最新数据，单独保存到他专属的 JSON 文件中"""
    user_data = mock_users_data.get(user_id)
    if not user_data:
        return
        
    # 获取当天日期，例如 20260313
    today_str = datetime.now().strftime('%Y%m%d')
    # 文件名格式：logs/user_1_20260313.json
    file_path = f"logs/user_{user_id}_{today_str}.json"
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)

# --- 模拟喂食接口 ---
@app.post("/activity/feed/{user_id}")
def feed(user_id: int):
    user = mock_users_data.get(user_id)
    if not user:
        return {"error": "用户未找到"}
        
    # 1. 更新用户业务数据：一次喂食增加10 [cite: 6]
    user["hunger"] += 10
    user["actions_today"] += 1
    
    # 2. 记录到全局总日志中
    logger.info(f"[集中日志] 用户 {user['nickname']} (ID:{user_id}) 进行了喂食，当前饥饿值: {user['hunger']}")
    
    # 3. 触发该用户的专属 JSON 文件更新
    save_user_data_to_json(user_id)
    
    return {"message": "喂食成功", "current_hunger": user["hunger"]}

app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")