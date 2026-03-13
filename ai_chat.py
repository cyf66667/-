import dashscope
from models import db_pet

# 请在此处填入你的阿里云 DashScope API Key
dashscope.api_key = "YOUR_DASHSCOPE_API_KEY"

def get_mood_description(mood_value: int) -> str:
    """根据心情值返回对应的情绪描述设定 """
    if 0 <= mood_value <= 30:
        return "特别不开心，语气低落、暴躁或委屈"
    elif 30 < mood_value <= 60:
        return "不开心，语气有些郁闷和敷衍"
    elif 60 < mood_value <= 80:
        return "正常情绪，语气平和自然"
    elif 80 < mood_value <= 100:
        return "开心，语气活泼、充满热情和依赖感"
    return "正常情绪"

def chat_with_luye(user_message: str):
    mood_desc = get_mood_description(db_pet.mood)
    
    # 构建 System Prompt，动态注入当前心情
    system_prompt = f"""
    你现在是我的电子宠物“鹿野”。
    你当前的心情值是 {db_pet.mood}/100。
    根据设定，你现在的状态是：{mood_desc}。
    请完全沉浸在这个情绪和角色中，用符合该心情的话术回答我的问题。
    """
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_message}
    ]
    
    try:
        response = dashscope.Generation.call(
            model='qwen-turbo',
            messages=messages,
            result_format='message'
        )
        return response.output.choices[0].message.content
    except Exception as e:
        return f"鹿野现在不想说话... (API调用失败: {str(e)})"