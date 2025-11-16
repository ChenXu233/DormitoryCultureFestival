from sqlalchemy import String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from typing import Dict, Optional, Any
from datetime import datetime

from backend.database import Base


class QuizResult(Base):
    __tablename__ = "quiz_results"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    participant_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    answers: Mapped[Dict[str, str]] = mapped_column(JSON)  # question_id: answer_index
    trait_scores: Mapped[Dict[str, Dict[str, int]]] = mapped_column(
        JSON
    )  # 维度: {特质: 分数}
    primary_traits: Mapped[Dict[str, str]] = mapped_column(JSON)  # 维度: 主要特质
    radar_data: Mapped[Dict[str, Any]] = mapped_column(JSON)  # 雷达图数据
    submitted_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


"""
answers 字段示例：
{
    "1": "2",  # 问题ID: 答案索引
    "2": "0"
}

trait_scores 字段示例：
{
    "生活习惯": {
        "整洁": 3,
        "随性": 1,
        "规律": 5,
        "灵活": 2
    },
    "社交倾向": {
        "外向": 4,
        "内向": 2,
        "平衡": 1,
        "选择性社交": 3
    }
}

primary_traits 字段示例：
{
    "生活习惯": "规律",
    "社交倾向": "外向"
}

radar_data 字段示例：
{
    "dimensions": ["生活习惯", "社交倾向", "作息规律", "学习风格", "娱乐偏好", "饮食习惯", "卫生习惯", "沟通方式"],
    "scores": [85, 70, 60, 45, 80, 55, 75, 65],
    "max_score": 100
}
"""
