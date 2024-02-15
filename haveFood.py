import datetime
import random

def ask_about_meal():
    # 获取当前时间
    now = datetime.datetime.now()
    
    # 定义不同时间段和相应的问题
    evening_be_questions = [
        "该休息了，天色已经很晚了。",
        "为了明天更好的精力，早点休息吧",
        "还没睡吗？已经这个时间了，你在美国吗？hh，不开玩笑了。",
    ]

    ermorning_questions = [
        "今天起的很早，还是失眠了？",
        "还不到七点，怎么了，不再睡一会儿吗？",
        "外面天亮了吗？还很早。",
    ]

    morning_questions = [
        "今天有什么计划吗？",
        "你今天一定有很想做的事情吧，如果没有，不如先去听一首歌。",
        "今天早饭好吃吗？",
    ]
    noon_questions = [
        "工作/学习做的怎么样了？",
        "如果累了，也请休息一下。",
    ]
    evening_questions = [
        "今天快要过去了，很不错哦，明天再接再厉。",
        "今天怎么样，不管顺利与否，都请期待明天哦。",
    ]
    
    # 根据当前时间决定问哪一餐的问题
    if now.hour < 4:
        # 早上
        question = random.choice(evening_be_questions)
    elif now.hour < 7:
        # 早上
        question = random.choice(ermorning_questions)
    elif now.hour < 10:
        # 早上
        question = random.choice(morning_questions)
    elif now.hour < 18:
        # 中午
        question = random.choice(noon_questions)
    else:
        # 晚上
        question = random.choice(evening_questions)
    
    return question

# # 打印问题
# print(ask_about_meal())
