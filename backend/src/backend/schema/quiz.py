from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime


class QuizQuestion(BaseModel):
    """答题问题模型"""

    id: int
    question: str
    options: List[str]
    traits: List[str]  # 关联的特质维度


class QuizSubmission(BaseModel):
    """答题提交模型"""

    participant_name: Optional[str] = None
    answers: Dict[str, str]  # question_id: answer_index
    submitted_at: Optional[datetime] = None


class TraitAnalysis(BaseModel):
    """特质分析模型"""

    traits: Dict[str, str]  # 维度: 主要特质
    compatibility_score: int
    match_analysis: List[str]


class MatchResult(BaseModel):
    """匹配结果模型"""

    code1: str
    code2: str
    participant1: str
    participant2: str
    compatibility_score: int
    traits1: Dict[str, str]
    traits2: Dict[str, str]
    match_analysis: List[str]
    message: str


class TeamMatchRequest(BaseModel):
    """团队匹配请求模型"""

    codes: List[str]  # 四个参与者的代码列表


class TeamMatchResult(BaseModel):
    """团队匹配结果模型"""

    team_compatibility_score: int
    team_trait_analysis: Dict[str, Any]
    team_commentary: Dict[str, str]
    participants: List[Dict[str, Any]]
    message: str
