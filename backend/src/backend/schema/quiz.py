from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class QuizQuestion(BaseModel):
    """答题问题模型"""

    id: int
    question: str
    options: List[str]
    category: str  # 问题分类，如：生活习惯、兴趣爱好等


class QuizSubmission(BaseModel):
    """答题提交模型"""

    dormitory_id: str  # 寝室ID
    participant_name: str  # 参与者姓名
    target_roommate: str  # 答题对象（哪个室友）
    answers: Dict[int, int]  # 问题ID到答案索引的映射
    submitted_at: datetime


class MatchResult(BaseModel):
    """匹配度结果模型"""

    match_score: int  # 匹配度分数（0-100）
    total_questions: int  # 总题数
    matched_answers: int  # 匹配的答案数
    match_percentage: float  # 匹配百分比
    time_spent: int  # 用时（秒）
    ranking: Optional[int] = None  # 排名
    match_level: str  # 匹配等级
    insights: List[str]  # 匹配度分析


class DormitoryMatchStats(BaseModel):
    """寝室匹配度统计"""

    dormitory_id: str
    total_participants: int
    average_match_score: float
    best_match_score: int
    total_submissions: int
    last_submission_time: datetime
    match_rankings: Dict[str, int]  # 各参与者匹配度排名
