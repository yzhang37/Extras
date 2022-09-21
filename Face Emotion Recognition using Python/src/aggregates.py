# 定义了各种各样的聚集函数
S_NEG = "Negative"
S_POS = "Positive"
S_NTL = "Neutral"


def aggregate_findmax(face_data: dict) -> dict:
    # 直接找最大值
    best_key = None
    best_value = 0.0
    for key, value in face_data.items():
        if value > best_value:
            best_key = key
            best_value = value
    return { best_key: best_value }


def aggregate_sum7to3(face_data: dict, surprise_is: str = S_NEG) -> dict:
    # 把几个数值相加再返回
    result = {}
    for key, value in face_data.items():
        new_key = {
            "angry": S_NEG,
            "disgust": S_NEG,
            "fear": S_NEG,
            "happy": S_POS,
            "neutral": S_NTL,
            "sad": S_NEG,
            "surprise": surprise_is
        }.get(key, None)
        if new_key is None:
            continue
        sum = result.get(new_key, 0.0)
        sum += value
        result[new_key] = sum
    return result


def mapping_customize(face_data: dict, angry: str, disgust: str, fear: str, happy: str, neutral: str, sad: str, surprise: str) -> dict:
    result = {}
    for key, value in face_data.items():
        new_key = {
            "angry": angry,
            "disgust": disgust,
            "fear": fear,
            "happy": happy,
            "neutral": neutral,
            "sad": sad,
            "surprise": surprise
        }.get(key, None)
        if new_key is None:
            continue
        result[new_key] = value
        break
    return result


def mapping_7to3(face_data: dict, surprise_is: str = S_NEG) -> dict:
    # 选择第一个 key, value, 然后改名字
    result = {}
    for key, value in face_data.items():
        new_key = {
            "angry": S_NEG,
            "disgust": S_NEG,
            "fear": S_NEG,
            "happy": S_POS,
            "neutral": S_NTL,
            "sad": S_NEG,
            "surprise": surprise_is
        }.get(key, None)
        if new_key is None:
            continue
        result[new_key] = value
        break
    return result