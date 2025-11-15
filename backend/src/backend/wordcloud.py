from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import json
import os

# 创建路由器
router = APIRouter(prefix="/api/wordcloud", tags=["wordcloud"])


# 数据模型
class WordCloudEntry(BaseModel):
    words: List[str] = Field(..., min_items=1, max_items=10)
    theme: Optional[dict] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = None


class WordCloudResponse(BaseModel):
    id: str
    words: List[dict]
    created_at: datetime


# 简单的存储实现（生产环境应该使用数据库）
class WordCloudStorage:
    def __init__(self):
        self.storage_file = "wordcloud_data.json"
        self.data = self._load_data()

    def _load_data(self):
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载词云数据失败: {e}")
        return {"entries": [], "word_frequencies": {}}

    def _save_data(self):
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"保存词云数据失败: {e}")

    def add_entry(self, entry: WordCloudEntry) -> str:
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
        # 转换词频数据为前端需要的格式
        return [
            {"text": word, "value": freq}
            for word, freq in self.data["word_frequencies"].items()
        ]

    def get_entry_by_id(self, entry_id: str) -> Optional[dict]:
        for entry in self.data["entries"]:
            if entry["id"] == entry_id:
                return entry
        return None


# 初始化存储
wordcloud_storage = WordCloudStorage()

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

# API路由


@router.post("/save", response_model=dict)
def save_wordcloud_entry(entry: WordCloudEntry):
    """保存用户的词云选择"""
    try:
        entry_id = wordcloud_storage.add_entry(entry)
        return {"id": entry_id, "message": "词云数据已保存"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")


@router.get("/global", response_model=List[dict])
def get_global_wordcloud():
    """获取全局词云数据（基于所有用户的选择）"""
    try:
        word_frequencies = wordcloud_storage.get_all_word_frequencies()
        # 如果还没有数据，返回预设词汇作为示例
        if not word_frequencies:
            return [
                {"text": word, "value": 10 + i % 20}
                for i, word in enumerate(PRESET_WORDS[:20])
            ]
        return word_frequencies
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取失败: {str(e)}")


@router.get("/words", response_model=List[str])
def get_preset_words():
    """获取预设的词汇列表"""
    return PRESET_WORDS


@router.get("/entry/{entry_id}", response_model=Optional[dict])
def get_wordcloud_entry(entry_id: str):
    """根据ID获取特定的词云条目"""
    entry = wordcloud_storage.get_entry_by_id(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="词云条目不存在")
    return entry
