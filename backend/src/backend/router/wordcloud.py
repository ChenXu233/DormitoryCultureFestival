from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..model.wordcloud import wordcloud_storage, PRESET_WORDS
from ..schema.wordcloud import WordCloudEntry


# 创建路由器
router = APIRouter(prefix="/api/wordcloud", tags=["wordcloud"])


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
