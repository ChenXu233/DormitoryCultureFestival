from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from typing import Dict

from backend.database import Base


class QuizResult(Base):
    __tablename__ = "quiz_results"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    result_data: Mapped[Dict[str, float]] = mapped_column(JSON)


"""
result_data 字段示例：
{
    "data":[
        {"question_id": 1, "selected_option": 2},
        {"question_id": 2, "selected_option": 0},
    ]
}
"""
