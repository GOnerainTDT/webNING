import requests
import random

good_temp = [
    "温度还算不错。",
    "是一个放风的好日子，你认为呢？",
    "今天的温度刚刚好，很适合外出。",
    "温度适中，非常舒适。",
    "这样的温度真是难得，不如抽个空去户外把。",
    "温暖而不炎热，凉爽而不寒冷，真是完美的一天。",
    "今天的天气让人感觉正好，既不冷也不热。",
    "温度这么舒服，正是出去散步的好时机。",
    "如此宜人的温度，真想整天都待在外面。",
    "今天的温度真合适，感觉四季如春。"
]

high_temp = [
    "今天真是热极了，尽量待在阴凉处吧。",
    "高温警报！记得多喝水，防中暑。",
    "今天温度好高，感觉要被晒化了。",
    "炎热的天气真让人受不了。",
    "今天出门必须带遮阳伞，太热了。",
    "高温天气，尽量减少户外活动。",
    "这么高的温度，空调房都不想出。",
    "今天的阳光实在太强烈了，皮肤都感觉到疼。",
    "温度太高了，感觉连空气都在燃烧。",
    "热浪滚滚，今天最好是宅在家里。"
]

low_temp = [
    "寒冷的天气，记得添衣保暖。",
    "低温警报，外出请穿厚衣服。",
    "今天真冷，冻得我直哆嗦。",
    "温度骤降，感觉冬天已经来了。",
    "这么低的温度，最好待在温暖的室内。",
    "寒风刺骨，尽量减少外出。",
    "低温天气，手脚冰凉，记得保暖。",
    "冷空气来袭，温度真的好低啊。",
    "今天外面冷得像冰箱，要穿得暖和一些。",
    "这种低温，最适合躲被窝里了。"
]

good_weather = [
    "天气真好，阳光明媚。",
    "今天是个好天气，适合出去玩。",
    "晴空万里，心情也跟着好起来。",
    "好天气，带上家人一起去野餐吧。",
    "今天天气晴朗，正好适合散步。",
    "阳光正好，微风不燥，真是完美的一天。",
    "这样的天气，去海边最好不过了。",
    "晴朗的天气让人心情愉悦。",
    "今天是出游的最佳天气，不热不冷。",
    "好天气，正是外出活动的好时机。"
]

bad_weather = [
    "今天天气不怎么样，最好还是待在家里。",
    "天气似乎很差，但也不要气馁，明天万一会变好呢。",
    "糟糕的天气，但也不要因此影响心情。",
    "天气看上去不太好，请多待在室内。",
    "老天爷似乎不太开心，请注意安全。",
    "阴天，感觉有点低落。",
    "恶劣的天气让人提不起精神来。",
    "今天外面风雨交加，真是糟糕透了。",
    "这样的天气，只想窝在家里。",
    "天气不太好，出行请小心。"
]


# def get_weather(city_name):
#     api_key = "cec5079c49910acac8ebe49a297c1ea0"
#     base_url = "http://api.openweathermap.org/data/2.5/weather?"
#     final_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=metric"
#     response = requests.get(final_url)
#     weather_data = response.json()
#     if weather_data['cod'] == 200:
#         temp = weather_data['main']['temp']
#         weather_description = weather_data['weather'][0]['description']
#         temp_message = ""
#         weather_message = ""

#         # 根据温度选择适当的句子
#         if temp > 30:
#             temp_message = random.choice(high_temp)
#         elif temp < 10:
#             temp_message = random.choice(low_temp)
#         else:
#             temp_message = random.choice(good_temp)

#         # 根据天气状况选择适当的句子
#         if "rain" in weather_description:
#             umbrella_message = "今天会下雨，别忘了带伞哦。"
#             weather_message = random.choice(bad_weather) + " " + umbrella_message
#         elif "storm" in weather_description:
#             weather_message += " " + random.choice(bad_weather) + " 注意安全，尽量避免外出。"
#         else:
#             weather_message += " " + random.choice(good_weather)


#         return f"{city_name}的当前温度是{temp}℃，{temp_message}天气状况：{weather_description}，{weather_message}"
#     else:
#         return "我不知道你现在在哪里，但也真切的希望，今天你所在的土地，仍旧晴空万里，花香四溢。"

def get_weather(city_name):
    api_key = "cec5079c49910acac8ebe49a297c1ea0"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    final_url = f"{base_url}appid={api_key}&q={city_name}&units=metric"
    if city_name == 'Unknown' or city_name == 'Error':
        return "我不知道你在哪里，希望你有个好天气。", "未知温度", "未知天气"
    
    try:
        response = requests.get(final_url)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        weather_data = response.json()
        temp = ''
        weather_description = ''
        if weather_data['cod'] == 200:
            temp = weather_data['main']['temp']
            weather_description = weather_data['weather'][0]['description']
        return weather_data, temp, weather_description
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return "天气服务暂时不可用，希望你那里能够有个好天气。", "未知温度", "未知天气"
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return "连接天气服务失败，但我希望你那里能够有个好天气。", "未知温度", "未知天气"
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
        return "连接天气服务超时，但我希望你那里能够有个好天气。", "未知温度", "未知天气"
    except requests.exceptions.RequestException as err:
        print("Oops: Something Else", err)
        return "获取天气信息不知道哪里出错了，但我希望你那里能够有个好天气。", "未知温度", "未知天气"
def get_weather_congratulations(city_name,weather_data):
    if weather_data['cod'] == 200:
        temp = weather_data['main']['temp']
        weather_description = weather_data['weather'][0]['description']
        temp_message = ""
        weather_message = ""

        # 根据温度选择适当的句子
        if temp > 30:
            temp_message = random.choice(high_temp)
        elif temp < 10:
            temp_message = random.choice(low_temp)
        else:
            temp_message = random.choice(good_temp)

        # 根据天气状况选择适当的句子
        if "rain" in weather_description:
            weather_message = random.choice(bad_weather) + " 今天会下雨，别忘了带伞哦。"
        elif "storm" in weather_description:
            weather_message = random.choice(bad_weather) + " 注意安全，尽量避免外出。"
        else:
            weather_message = random.choice(good_weather)

        return f"{city_name}的当前温度是{temp}℃，{temp_message} 天气状况：{weather_description}，{weather_message}"
    else:
        return "我不知道你现在在哪里，但也真切的希望，今天你所在的土地，仍旧晴空万里，花香四溢。"

if __name__ == '__main__':
    weather_data, temp, weather_description = get_weather("Shenyang")
    print(weather_data, temp, weather_description)
    print(get_weather_congratulations("Shenyang",weather_data))
# # 示例：获取"北京"的天气
# print(get_weather("Shenyang"))
