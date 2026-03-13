import time
import random
import requests
import threading

# 在 Docker 网络中，我们可以直接通过服务名 'api' 访问后端
API_BASE_URL = "http://api:8000"

# 模拟 10 名用户的基本信息
users = [{"user_id": i, "nickname": f"玩家_{i:03d}"} for i in range(1, 11)]

def simulate_user_behavior(user):
    """模拟单个用户的随机行为"""
    while True:
        try:
            # 随机决定当前用户是否“上线”游玩 (30% 概率在线)
            if random.random() < 0.3:
                print(f"[{user['nickname']}] 上线了，开始互动...")
                
                # 随机进行 1 到 5 次操作
                actions_count = random.randint(1, 5)
                for _ in range(actions_count):
                    action = random.choice(["/activity/feed", "/activity/water", "/activity/play", "/training/train"])
                    
                    # 发送请求给后端 API
                    response = requests.post(f"{API_BASE_URL}{action}")
                    print(f"[{user['nickname']}] 执行了 {action} -> 结果: {response.status_code}")
                    
                    # 每次操作间隔 2-5 秒
                    time.sleep(random.randint(2, 5))
                
                print(f"[{user['nickname']}] 游玩结束，下线休息。")
            
            # 无论是否上线，都休息一段时间（模拟现实中的时间流逝，这里缩短为 10-30 秒方便观察）
            time.sleep(random.randint(10, 30))
            
        except requests.exceptions.ConnectionError:
            print("等待 API 服务启动...")
            time.sleep(5)

if __name__ == "__main__":
    print("🚀 鹿野养成计划 - 10人模拟器启动！")
    # 为每个用户开启一个线程，模拟并发游玩
    threads = []
    for user in users:
        t = threading.Thread(target=simulate_user_behavior, args=(user,))
        t.daemon = True
        t.start()
        threads.append(t)
    
    # 保持主线程运行
    while True:
        time.sleep(1)