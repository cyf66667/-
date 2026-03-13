import random
from models import db_pet

def feed_pet():
    """一次喂食增加10点饥饿值（视作饱食度增加） [cite: 6]"""
    db_pet.hunger += 10
    return {"message": "喂食成功", "current_hunger": db_pet.hunger}

def water_pet():
    """一次喂水增加10点口渴值（视作解渴度增加） [cite: 6]"""
    db_pet.thirst += 10
    return {"message": "喂水成功", "current_thirst": db_pet.thirst}

def play_with_pet():
    """玩耍逻辑 """
    db_pet.mood = min(100, db_pet.mood + 10)
    db_pet.hunger -= 5 # 玩耍消耗体力
    return {"message": "玩耍成功", "current_mood": db_pet.mood}

def train_pet():
    """
    练功逻辑处理
    第一级：婴儿模式无法练功 
    第二级：少年模式可练功，18岁前等级上限80，生命值上升为150 
    第三级：青年模式可练功到满级，生命值上升到200 
    """
    if db_pet.stage == 1:
        return {"error": "婴儿模式无法练功"}
    
    # 练功增加饥饿值（模拟体力消耗） [cite: 8]
    db_pet.hunger -= 5 
    db_pet.training_time += 1
    
    if db_pet.stage == 2:
        if db_pet.training_level < 80:
            db_pet.training_level += 1
        db_pet.health = 150  # 提升生命值上限
        return {"message": "少年模式练功成功", "level": db_pet.training_level, "health": db_pet.health}
        
    if db_pet.stage == 3:
        # 假设满级为 100
        if db_pet.training_level < 100:
            db_pet.training_level += 1
        db_pet.health = 200  # 提升生命值上限
        return {"message": "青年模式练功成功", "level": db_pet.training_level, "health": db_pet.health}

def refresh_daily_mood():
    """每天随机刷新心情值 (0-100) [cite: 3]"""
    db_pet.mood = random.randint(0, 100)
    return {"message": "心情已刷新", "new_mood": db_pet.mood}