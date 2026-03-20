import tkinter as tk
import random

class LuYeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("鹿野养成计划 - 桌面测试版")
        self.root.geometry("350x520")
        
        # 1. 初始核心数据
        self.health = 100
        self.hunger = 50
        self.thirst = 50
        self.mood = 80
        
        # 阶段与练功数据
        self.stage = 2
        self.level = 0
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # --- 状态展示区 ---
        self.info_frame = tk.LabelFrame(self.root, text="🦌 鹿野当前状态", padx=10, pady=10)
        self.info_frame.pack(fill="x", padx=15, pady=10)
        
        self.health_label = tk.Label(self.info_frame, text="生命值: ", font=("Arial", 12))
        self.health_label.pack(anchor="w")
        
        self.hunger_label = tk.Label(self.info_frame, text="饥饿程度: ", font=("Arial", 12))
        self.hunger_label.pack(anchor="w")
        
        self.thirst_label = tk.Label(self.info_frame, text="口渴程度: ", font=("Arial", 12))
        self.thirst_label.pack(anchor="w")
        
        self.level_label = tk.Label(self.info_frame, text="练功等级: ", font=("Arial", 12))
        self.level_label.pack(anchor="w")
        
        self.mood_label = tk.Label(self.info_frame, text="心情值: ", font=("Arial", 12, "bold"), fg="blue")
        self.mood_label.pack(anchor="w", pady=(10, 0))

        # --- 交互操作区 ---
        self.action_frame = tk.LabelFrame(self.root, text="🕹️ 互动操作", padx=10, pady=10)
        self.action_frame.pack(fill="x", padx=15, pady=10)
        
        # 活动板块 
        tk.Button(self.action_frame, text="🍚 喂食 (降饥饿, 升心情)", command=self.feed).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.action_frame, text="💧 喂水 (降口渴)", command=self.water).grid(row=0, column=1, padx=5, pady=5)
        
        # 练功板块 
        tk.Button(self.action_frame, text="⚔️ 练功 (升饥饿)", command=self.train).grid(row=1, column=0, columnspan=2, sticky="we", padx=5, pady=5)
        
        # --- 时间与系统控制区 ---
        self.system_frame = tk.LabelFrame(self.root, text="⏳ 系统机制测试", padx=10, pady=10)
        self.system_frame.pack(fill="x", padx=15, pady=10)

        # 模拟时间流逝
        tk.Button(self.system_frame, text="模拟度过 1 小时", command=self.pass_one_hour, bg="#ffedcc").pack(fill="x", pady=5)
        
        # 模拟每日刷新
        tk.Button(self.system_frame, text="模拟跨天 (随机刷新心情)", command=self.refresh_mood, bg="#e0e0e0").pack(fill="x", pady=5)

    # --- 核心逻辑 ---
    def feed(self):
        # 1. 减少饥饿值，随机范围 2 到 15
        hunger_decrease = random.randint(2, 15)
        self.hunger -= hunger_decrease
        if self.hunger < 0:
            self.hunger = 0
            
        # 2. 增加心情值，随机范围 5 到 15
        mood_increase = random.randint(5, 15)
        self.mood += mood_increase
        # 上限保护，最高为 100
        if self.mood > 100:
            self.mood = 100
            
        self.update_display()

    def water(self):
        # 减少口渴值，随机范围 2 到 15
        amount = random.randint(2, 15)
        self.thirst -= amount
        if self.thirst < 0:
            self.thirst = 0
        self.update_display()

    def train(self):
        # 练功增加饥饿程度
        self.hunger += 10 
        if self.hunger > 100:
            self.hunger = 100
        
        if self.stage == 2:
            if self.level < 80:
                self.level += 1
            self.health = 150
            
        self.update_display()

    def pass_one_hour(self):
        # 随着时间流逝，饥饿和口渴自然上升
        self.hunger = min(100, self.hunger + 5)
        self.thirst = min(100, self.thirst + 5)

        # 饥饿值过高(>60)时扣除心情
        if self.hunger > 60:
            self.mood -= 10
            if self.mood < 0:
                self.mood = 0

        if self.thirst > 60:
            self.mood -= 10
            if self.mood < 0:
                self.mood = 0

        self.update_display()

    def refresh_mood(self):
        # 每天随机刷新心情值 0-100
        self.mood = random.randint(0, 100)
        self.update_display()

    def get_mood_text(self):
        if 0 <= self.mood <= 30:
            return "特别不开心 😭"
        elif 30 < self.mood <= 60:
            return "不开心 😞"
        elif 60 < self.mood <= 80:
            return "正常情绪 😐"
        elif 80 <= self.mood <= 100:
            return "开心 😊"
        return ""

    def update_display(self):
        self.health_label.config(text=f"生命值: {self.health}")
        self.hunger_label.config(text=f"饥饿程度: {self.hunger} / 100")
        self.thirst_label.config(text=f"口渴程度: {self.thirst} / 100")
        self.level_label.config(text=f"练功等级: LV.{self.level}")
        
        mood_desc = self.get_mood_text()
        self.mood_label.config(text=f"心情值: {self.mood} ({mood_desc})")

if __name__ == "__main__":
    root = tk.Tk()
    app = LuYeApp(root)
    root.mainloop()