import json
import os
import random
from typing import Dict, List, Optional

GENERAL: List[str] = [
    "你好呀~", "今天天气不错！", "嗨！想我了吗？",
    "终于等到你啦！", "好久不见！", "嘿嘿~",
    "哎呀！", "呜呜...", "耶！", "诶嘿☆",
    "来抓我呀~", "好无聊啊...", "陪我玩！", "别点啦~",
    "你点不到我~", "我好可爱对不对~", "加油！", "你最棒了！",
    "休息一下吧~", "今天辛苦了！", "我是一团小可爱~",
    "点击有惊喜！", "困了...zzZ", "咕噜咕噜~",
    "不要戳我的脸！", "再点我就生气了！", "我饿了...有零食吗？",
    "相信自己！", "慢慢来，不着急~", "你一定能做到的！",
    "今天想做什么呢？", "快来和我一起玩耍！",
    "嘻，被你发现了~", "嘿嘿，好痒~",
    "今天也是可爱的一天！", "有人在家吗？",
]

DOUBLE_CLICK: List[str] = [
    "哇！你好热情！", "别急别急~", "双击超棒！",
    "兴奋得转圈圈！", "阿嚏——！好大的喷嚏", "停停停，我要晕了！",
    "再来一次！", "哇哦~~超开心！", "你找到隐藏动作啦！",
    "好厉害的连击！",
]

WANDER: List[str] = [
    "溜达溜达~", "出去转转", "那是什么？去看看",
    "散步时间到！", "换个地方待会儿", "我要去看看那边",
    "咦？有东西在闪", "坐太久啦，活动一下",
    "饭后百步走~",
]

IDLE: List[str] = [
    "好安静啊...", "有没有人呀~", "犯困了...zzZZ",
    "发呆中...", "我在思考人生", "今天的云好漂亮",
    "你还在吗？", "要不要一起玩？", "好想喝奶茶...",
    "什么时候下班呀~", "有点小饿...",
]

CATEGORY_MAP: Dict[str, List[str]] = {
    "general": GENERAL,
    "double_click": DOUBLE_CLICK,
    "wander": WANDER,
    "idle": IDLE,
}

_skin_phrases_cache: Dict[str, List[str]] = {}


def _load_skin_phrases(skin_dir: str) -> List[str]:
    if skin_dir in _skin_phrases_cache:
        return _skin_phrases_cache[skin_dir]
    phrase_file = os.path.join(skin_dir, "phrases.json")
    if os.path.exists(phrase_file):
        try:
            with open(phrase_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                _skin_phrases_cache[skin_dir] = data
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


def get_random_phrase(skin_dir: str = "") -> str:
    if skin_dir:
        phrases = _load_skin_phrases(skin_dir)
        if phrases:
            return random.choice(phrases)
    return ""  # 无皮肤专属短语时不说话


def get_phrase(category: str, skin_dir: str = "") -> str:
    if skin_dir:
        phrases = _load_skin_phrases(skin_dir)
        if phrases:
            return random.choice(phrases)
    return ""  # 无皮肤专属短语时不说话
