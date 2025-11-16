import json
import os
from datetime import datetime
from typing import List, Optional
from ..schema.wordcloud import WordCloudEntry


class WordCloudStorage:
    """词云数据存储类"""

    def __init__(self):
        self.storage_file = "wordcloud_data.json"
        self.data = self._load_data()

    def _load_data(self):
        """加载词云数据"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # 兼容旧版本数据格式，确保有word_frequencies字段
                    if "word_frequencies" not in data:
                        data["word_frequencies"] = {}
                    return data
        except Exception as e:
            print(f"加载词云数据失败: {e}")
        return {"word_frequencies": {}}

    def _save_data(self):
        """保存词云数据到文件"""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"保存词云数据失败: {e}")

    def add_entry(self, entry: WordCloudEntry) -> str:
        """添加词云条目 - 只更新词频统计，不保存具体条目"""
        # 更新词频统计
        for word in entry.words:
            if word in self.data["word_frequencies"]:
                self.data["word_frequencies"][word] += 1
            else:
                self.data["word_frequencies"][word] = 1

        # 保存到文件
        self._save_data()
        return "success"

    def get_all_word_frequencies(self) -> List[dict]:
        """获取所有词频数据"""
        # 转换词频数据为前端需要的格式
        return [
            {"text": word, "value": freq}
            for word, freq in self.data["word_frequencies"].items()
        ]

    def get_entry_by_id(self, entry_id: str) -> Optional[dict]:
        """根据ID获取词云条目 - 已弃用，不再保存具体条目"""
        return None


# 预设词汇列表
PRESET_WORDS = [
    "带饭侠",
    "静音大师",
    "节能标兵",
    "整洁担当",
    "人形闹钟",
    "关灯使者",
    "鼾声歌者",
    "学霸之光",
    "DDL警长",
    "占座先锋",
    "笔记富翁",
    "小组大腿",
    "学渣救星",
    "夸夸团主",
    "台阶建造师",
    "情绪稳定剂",
    "废话树洞",
    "八卦雷达",
    "防社死专员",
    "宿舍梗王",
    "美食地图",
    "氛围担当",
    "戏精本精",
    "养生专家",
    "游戏大神",
    "平账大师",
    "火锅局长",
    "零食国库",
    "查寝先知",
    "维修客",
    "砍价能手",
    "人形快递柜",
    "早起鸟",
    "夜猫子",
    "二手市场",
    "试毒官",
    "非著名摄影师",
    "麦霸",
    "人间充电宝",
]


# 初始化存储实例
wordcloud_storage = WordCloudStorage()
