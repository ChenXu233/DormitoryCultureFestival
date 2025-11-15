from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class WordCloudEntry(BaseModel):
    """词云条目数据模型"""

    words: List[str] = Field(..., min_items=1, max_items=10)
    theme: Optional[dict] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = None


class WordCloudResponse(BaseModel):
    """词云响应数据模型"""

    id: str
    words: List[dict]
    created_at: datetime
