from pydantic import BaseModel
from typing import Dict, List, Optional, Any


class GroupCompatibilityRequest(BaseModel):
    """群体兼容性请求模型"""
    codes: List[str]


class MemberInfo(BaseModel):
    """成员信息模型"""
    code: str
    participant_name: Optional[str]
    primary_traits: Dict[str, str]
    trait_scores: Dict[str, Dict[str, int]]


class BestPair(BaseModel):
    """最佳配对模型"""
    member1_code: str
    member2_code: str
    common_traits_count: int
    common_dimensions: List[str]
    compatibility_score: int


class GroupCompatibilityResponse(BaseModel):
    """群体兼容性响应模型"""
    codes: List[str]
    avg_compatibility_score: int
    group_compatibility: Dict[str, Any]
    best_pairs: List[BestPair]
    members_info: List[MemberInfo]
    message: str