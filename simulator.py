import time
import random
import requests
import threading
from datetime import datetime

# 在 Docker 的桥接网络中，直接使用服务名 'api' 即可访问后端
BASE_URL = "http://luye_api:8000"  # 注意：把 127.0.0.1 换成了 luye_api

def simulate_user_behavior(user_id, nickname):
    """模拟单个虚拟玩家的行为"""
    while True:
        try:
            # 模拟玩家随机决定当前是否“上线”游玩 (30% 概率在线)
            if random.random() < 0.3:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎮 {nickname} 上线了，开始照顾鹿野...")
                
                # 上线后，随机进行 1 到 3 次互动
                actions_count = random.randint(1, 3)
                for _ in range(actions_count):
                    # 随机选择喂饭还是喂水
                    action = random.choice(["feed", "water"])
                    url = f"{BASE_URL}/activity/{action}/{user_id}"
                    
                    # 向 API 发送动作指令
                    response = requests.post(url)
                    
                    # 解析后端的真实生理反馈
                    if response.status_code == 200:
                        data = response.json()
                        msg = data.get("message", "操作成功")
                        timestamp = data.get("timestamp", "")
                        print(f"  -> [{timestamp}] {nickname} : {msg}")
                    else:
                        print(f"  -> {nickname} 请求出错，状态码: {response.status_code}")
                    
                    # 每次操作之间停顿几秒，模拟人类操作的延迟
                    time.sleep(random.randint(2, 5))
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 💤 {nickname} 游玩结束，下线休息。")
            
            # 无论刚才是否上线，都让线程休息 10 到 20 秒（为了快速看效果，时间设得比较短）
            time.sleep(random.randint(10, 20))
            
        except requests.exceptions.ConnectionError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 正在等待 API 服务启动...")
            time.sleep(5)

if __name__ == "__main__":
    print("🚀 鹿野养成计划 - 10人高并发模拟器启动！开始制造带时间戳的真实测试数据...")
    
    threads = []
    # 循环创建 10 个虚拟玩家的线程
    for i in range(1, 11):
        nickname = f"玩家_{i:03d}"
        t = threading.Thread(target=simulate_user_behavior, args=(i, nickname))
        t.daemon = True  # 设置为守护线程，主程序退出时一起退出
        t.start()
        threads.append(t)
    
    # 保持主线程一直存活，让 10 个玩家在后台不断循环游玩
    while True:
        time.sleep(1)