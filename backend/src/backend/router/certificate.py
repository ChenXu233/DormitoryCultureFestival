from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..model.quiz import QuizResult
from ..database import async_session
from ..schema.certificate import GroupCompatibilityRequest, GroupCompatibilityResponse

router = APIRouter(prefix="/certificate", tags=["证书模块"])

# 数据库会话依赖
async def get_db():
    async with async_session() as session:
        yield session


def calculate_group_compatibility(traits_list: List[Dict[str, str]]) -> Dict[str, Any]:
    """计算寝室成员群体兼容性"""
    if not traits_list or len(traits_list) < 2:
        return {"compatibility_score": 0, "analysis": []}
    
    # 统计每个维度的特质分布
    dimension_traits = {}
    for traits in traits_list:
        for dimension, trait in traits.items():
            if dimension not in dimension_traits:
                dimension_traits[dimension] = {}
            if trait not in dimension_traits[dimension]:
                dimension_traits[dimension][trait] = 0
            dimension_traits[dimension][trait] += 1
    
    # 计算群体兼容性得分
    total_score = 0
    max_possible_score = 0
    analysis = []
    
    for dimension, traits in dimension_traits.items():
        # 计算该维度的多样性指数
        total_members = sum(traits.values())
        if total_members == 0:
            continue
            
        # 计算该维度的一致性得分（相同特质越多得分越高）
        consistency_score = max(traits.values()) / total_members
        total_score += consistency_score
        max_possible_score += 1
        
        # 添加分析
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_traits) == 1:
            analysis.append(f"{dimension}：全体成员都是{sorted_traits[0][0]}，高度一致！")
        elif sorted_traits[0][1] > total_members * 0.6:
            analysis.append(f"{dimension}：大多数成员({sorted_traits[0][1]}人)是{sorted_traits[0][0]}，较为统一")
        else:
            trait_desc = "、".join([f"{trait}({count}人)" for trait, count in sorted_traits[:3]])
            analysis.append(f"{dimension}：成员特质多样，包括{trait_desc}，互补性强")
    
    # 计算最终兼容性得分（0-100）
    compatibility_score = int((total_score / max_possible_score) * 100) if max_possible_score > 0 else 0
    
    return {
        "compatibility_score": compatibility_score,
        "analysis": analysis
    }


def find_best_pairs(traits_list: List[Dict[str, str]], codes: List[str]) -> List[Dict[str, Any]]:
    """找出最佳配对"""
    if len(traits_list) < 2:
        return []
    
    pairs = []
    # 简单实现：找出具有最多共同特质的配对
    for i in range(len(traits_list)):
        for j in range(i + 1, len(traits_list)):
            traits1 = traits_list[i]
            traits2 = traits_list[j]
            
            common_traits = 0
            common_dimensions = []
            
            for dimension in traits1:
                if dimension in traits2 and traits1[dimension] == traits2[dimension]:
                    common_traits += 1
                    common_dimensions.append(dimension)
            
            pairs.append({
                "member1_code": codes[i],
                "member2_code": codes[j],
                "common_traits_count": common_traits,
                "common_dimensions": common_dimensions,
                "compatibility_score": int((common_traits / max(len(traits1), len(traits2))) * 100) if traits1 and traits2 else 0
            })
    
    # 按兼容性得分排序，返回前几个最佳配对
    pairs.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return pairs[:3]  # 返回前3个最佳配对


@router.post("/group-compatibility", response_model=GroupCompatibilityResponse)
async def calculate_group_compatibility_endpoint(
    request: GroupCompatibilityRequest, 
    db: AsyncSession = Depends(get_db)
):
    """计算寝室群体兼容性
    接收四个舍友代码，查询数据库中的答题数据，并计算群体特质近似度
    """
    codes = request.codes
    if len(codes) != 4:
        raise HTTPException(status_code=400, detail="需要提供 exactly 4 个舍友代码")
    
    # 查询数据库获取所有成员的答题数据
    members_data = []
    for code in codes:
        result = await db.execute(select(QuizResult).where(QuizResult.code == code))
        member = result.scalar_one_or_none()
        if not member:
            raise HTTPException(status_code=404, detail=f"未找到代码为 {code} 的成员数据")
        members_data.append(member)
    
    # 提取所有成员的主要特质
    traits_list = [member.primary_traits for member in members_data]
    
    # 计算群体兼容性
    compatibility_result = calculate_group_compatibility(traits_list)
    
    # 找出最佳配对
    best_pairs = find_best_pairs(traits_list, codes)
    
    # 计算平均兼容性得分
    avg_compatibility = sum([calculate_group_compatibility([t])["compatibility_score"] for t in traits_list]) // len(traits_list)
    
    return GroupCompatibilityResponse(
        codes=codes,
        avg_compatibility_score=avg_compatibility,
        group_compatibility=compatibility_result,
        best_pairs=best_pairs,
        members_info=[
            {
                "code": member.code,
                "participant_name": member.participant_name or "匿名用户",
                "primary_traits": member.primary_traits,
                "trait_scores": member.trait_scores
            }
            for member in members_data
        ],
        message=f"寝室群体兼容性分析完成！整体兼容性得分为：{compatibility_result['compatibility_score']}%"
    )