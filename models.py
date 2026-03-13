from pydantic import BaseModel

class PetState(BaseModel):
    name: str = "鹿野"
    age: int = 0                  # 这里的 age 可以代表天数或具体岁数
    stage: int = 1                # 1: 婴儿, 2: 少年(18岁前), 3: 青年
    form: str = "婴儿期形态"       # 每到一个时期改变一次形态 [cite: 11]
    
    health: int = 100             # 初始生命值100 
    hunger: int = 0               # 饥饿值
    thirst: int = 0               # 口渴值
    mood: int = 80                # 心情值 (0-100) [cite: 3]
    
    training_level: int = 0       # 练功等级
    training_time: int = 0        # 累计练功时间

# 全局内存模拟数据库（实际开发请替换为 MySQL/SQLite）
db_pet = PetState()