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
                    return json.load(f)
        except Exception as e:
            print(f"加载词云数据失败: {e}")
        return {"entries": [], "word_frequencies": {}}

    def _save_data(self):
        """保存词云数据到文件"""
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"保存词云数据失败: {e}")

    def add_entry(self, entry: WordCloudEntry) -> str:
        """添加词云条目"""
        # 生成简单的ID
        entry_id = f"wc_{datetime.now().timestamp()}"

        # 更新词频统计
        for word in entry.words:
            if word in self.data["word_frequencies"]:
                self.data["word_frequencies"][word] += 1
            else:
                self.data["word_frequencies"][word] = 1

        # 保存条目
        self.data["entries"].append(
            {
                "id": entry_id,
                "words": entry.words,
                "theme": entry.theme,
                "created_at": entry.created_at.isoformat(),
                "session_id": entry.session_id,
            }
        )

        # 保存到文件
        self._save_data()
        return entry_id

    def get_all_word_frequencies(self) -> List[dict]:
        """获取所有词频数据"""
        # 转换词频数据为前端需要的格式
        return [
            {"text": word, "value": freq}
            for word, freq in self.data["word_frequencies"].items()
        ]

    def get_entry_by_id(self, entry_id: str) -> Optional[dict]:
        """根据ID获取词云条目"""
        for entry in self.data["entries"]:
            if entry["id"] == entry_id:
                return entry
        return None


# 预设词汇列表
PRESET_WORDS = [
    "友善",
    "幽默",
    "责任心",
    "细心",
    "热情",
    "开朗",
    "善解人意",
    "聪明",
    "勤奋",
    "乐观",
    "诚实",
    "正直",
    "可靠",
    "慷慨",
    "耐心",
    "积极",
    "理性",
    "感性",
    "稳重",
    "活泼",
    "冷静",
    "外向",
    "内向",
    "独立",
    "合作",
    "创新",
    "踏实",
    "细心",
    "有条理",
    "整洁",
    "爱干净",
    "有趣",
    "健谈",
    "安静",
    "乐于助人",
    "善解人意",
    "有同理心",
    "有爱心",
    "有正义感",
    "有创造力",
    "有领导力",
    "有团队精神",
    "有毅力",
    "有耐心",
    "有幽默感",
    "有品味",
    "有活力",
    "温柔",
    "坚强",
    "勇敢",
]


# 初始化存储实例
wordcloud_storage = WordCloudStorage()
