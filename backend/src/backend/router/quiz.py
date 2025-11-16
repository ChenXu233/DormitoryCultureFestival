from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime
import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schema.quiz import QuizQuestion, QuizSubmission, MatchResult
from ..model.quiz import QuizResult
from ..database import async_session

router = APIRouter(prefix="/quiz", tags=["答题模块"])

# 特质维度定义
TRAIT_DIMENSIONS = {
    "生活习惯": ["整洁", "随性", "规律", "灵活"],
    "社交倾向": ["外向", "内向", "平衡", "选择性社交"],
    "作息规律": ["早睡早起", "夜猫子", "规律作息", "弹性作息"],
    "学习风格": ["独立学习", "小组学习", "视觉学习", "听觉学习"],
    "娱乐偏好": ["安静活动", "户外活动", "社交活动", "创意活动"],
    "饮食习惯": ["健康饮食", "随意饮食", "美食家", "简单饮食"],
    "卫生习惯": ["高度整洁", "适度整洁", "随性", "注重细节"],
    "沟通方式": ["直接沟通", "委婉沟通", "书面沟通", "行动沟通"],
}

# 题库数据 - 通过答题推断个人特质
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "你通常如何度过周末？",
        "options": ["宅在寝室休息", "和朋友外出聚会", "学习或工作", "参加户外活动"],
        "traits": ["生活习惯", "社交倾向", "娱乐偏好"],
    },
    {
        "id": 2,
        "question": "你的学习习惯是怎样的？",
        "options": ["独自安静学习", "喜欢小组讨论", "边听音乐边学习", "需要完全安静"],
        "traits": ["学习风格", "生活习惯"],
    },
    {
        "id": 3,
        "question": "你整理个人物品的频率是？",
        "options": ["每天整理", "2-3天一次", "每周整理", "需要时才整理"],
        "traits": ["卫生习惯", "生活习惯"],
    },
    {
        "id": 4,
        "question": "你更喜欢哪种社交方式？",
        "options": ["大型聚会", "小范围聊天", "一对一交流", "线上社交"],
        "traits": ["社交倾向", "沟通方式"],
    },
    {
        "id": 5,
        "question": "你的作息时间通常是？",
        "options": ["22:00前睡觉", "22:00-24:00睡觉", "24:00-2:00睡觉", "2:00后睡觉"],
        "traits": ["作息规律", "生活习惯"],
    },
    {
        "id": 6,
        "question": "你选择食物时最看重什么？",
        "options": ["健康营养", "口味美味", "方便快捷", "价格实惠"],
        "traits": ["饮食习惯", "生活习惯"],
    },
    {
        "id": 7,
        "question": "遇到问题时，你通常如何解决？",
        "options": ["直接说出来", "委婉表达", "写下来思考", "先观察再行动"],
        "traits": ["沟通方式", "学习风格"],
    },
    {
        "id": 8,
        "question": "你最喜欢的放松方式是什么？",
        "options": ["听音乐/看书", "运动健身", "和朋友聊天", "玩游戏/看电影"],
        "traits": ["娱乐偏好", "社交倾向"],
    },
    {
        "id": 9,
        "question": "你对个人空间的整洁度要求？",
        "options": ["必须一尘不染", "保持基本整洁", "舒适即可", "不太在意"],
        "traits": ["卫生习惯", "生活习惯"],
    },
    {
        "id": 10,
        "question": "你更喜欢哪种学习环境？",
        "options": ["完全安静", "有背景音乐", "与人讨论", "户外环境"],
        "traits": ["学习风格", "娱乐偏好"],
    },
]


# 数据库会话依赖
async def get_db():
    async with async_session() as session:
        yield session


async def generate_4_digit_code(db: AsyncSession):
    """生成4位唯一代码，确保在数据库中唯一"""
    max_attempts = 100  # 最大尝试次数，避免无限循环
    attempts = 0

    while attempts < max_attempts:
        # 使用数字和字母组合，确保4位代码足够唯一
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

        # 检查数据库中是否已存在该代码
        result = await db.execute(select(QuizResult).where(QuizResult.code == code))
        existing_code = result.scalar_one_or_none()

        if not existing_code:
            return code

        attempts += 1

    # 如果尝试次数过多，使用时间戳+随机数生成更长的唯一代码
    timestamp = int(datetime.now().timestamp())
    fallback_code = f"{timestamp}{random.randint(1000, 9999)}"
    return fallback_code


def analyze_traits(answers):
    """分析答题结果，推断个人特质并计算分数"""
    # 初始化特质分数
    trait_scores = {
        dimension: {trait: 0 for trait in traits}
        for dimension, traits in TRAIT_DIMENSIONS.items()
    }

    # 定义答案与特质的映射关系
    answer_trait_mapping = {
        # 问题1: 你通常如何度过周末？
        1: {
            0: {"生活习惯": "规律", "娱乐偏好": "安静活动"},
            1: {"生活习惯": "灵活", "社交倾向": "外向", "娱乐偏好": "社交活动"},
            2: {"生活习惯": "规律", "学习风格": "独立学习"},
            3: {"生活习惯": "灵活", "娱乐偏好": "户外活动"},
        },
        # 问题2: 你的学习习惯是怎样的？
        2: {
            0: {"学习风格": "独立学习", "生活习惯": "规律"},
            1: {"学习风格": "小组学习", "社交倾向": "外向"},
            2: {"学习风格": "听觉学习", "生活习惯": "灵活"},
            3: {"学习风格": "视觉学习", "生活习惯": "规律"},
        },
        # 问题3: 你整理个人物品的频率是？
        3: {
            0: {"卫生习惯": "高度整洁", "生活习惯": "规律"},
            1: {"卫生习惯": "适度整洁", "生活习惯": "规律"},
            2: {"卫生习惯": "适度整洁", "生活习惯": "灵活"},
            3: {"卫生习惯": "随性", "生活习惯": "灵活"},
        },
        # 问题4: 你更喜欢哪种社交方式？
        4: {
            0: {"社交倾向": "外向", "沟通方式": "直接沟通"},
            1: {"社交倾向": "平衡", "沟通方式": "委婉沟通"},
            2: {"社交倾向": "内向", "沟通方式": "委婉沟通"},
            3: {"社交倾向": "选择性社交", "沟通方式": "书面沟通"},
        },
        # 问题5: 你的作息时间通常是？
        5: {
            0: {"作息规律": "早睡早起", "生活习惯": "规律"},
            1: {"作息规律": "规律作息", "生活习惯": "规律"},
            2: {"作息规律": "弹性作息", "生活习惯": "灵活"},
            3: {"作息规律": "夜猫子", "生活习惯": "灵活"},
        },
        # 问题6: 你选择食物时最看重什么？
        6: {
            0: {"饮食习惯": "健康饮食", "生活习惯": "规律"},
            1: {"饮食习惯": "美食家", "生活习惯": "灵活"},
            2: {"饮食习惯": "简单饮食", "生活习惯": "灵活"},
            3: {"饮食习惯": "随意饮食", "生活习惯": "灵活"},
        },
        # 问题7: 遇到问题时，你通常如何解决？
        7: {
            0: {"沟通方式": "直接沟通", "社交倾向": "外向"},
            1: {"沟通方式": "委婉沟通", "社交倾向": "平衡"},
            2: {"沟通方式": "书面沟通", "学习风格": "视觉学习"},
            3: {"沟通方式": "行动沟通", "学习风格": "独立学习"},
        },
        # 问题8: 你最喜欢的放松方式是什么？
        8: {
            0: {"娱乐偏好": "安静活动", "社交倾向": "内向"},
            1: {"娱乐偏好": "户外活动", "社交倾向": "外向"},
            2: {"娱乐偏好": "社交活动", "社交倾向": "外向"},
            3: {"娱乐偏好": "创意活动", "学习风格": "视觉学习"},
        },
        # 问题9: 你对个人空间的整洁度要求？
        9: {
            0: {"卫生习惯": "高度整洁", "生活习惯": "规律"},
            1: {"卫生习惯": "适度整洁", "生活习惯": "规律"},
            2: {"卫生习惯": "适度整洁", "生活习惯": "灵活"},
            3: {"卫生习惯": "随性", "生活习惯": "灵活"},
        },
        # 问题10: 你更喜欢哪种学习环境？
        10: {
            0: {"学习风格": "独立学习", "社交倾向": "内向"},
            1: {"学习风格": "听觉学习", "生活习惯": "灵活"},
            2: {"学习风格": "小组学习", "社交倾向": "外向"},
            3: {"学习风格": "视觉学习", "娱乐偏好": "户外活动"},
        },
    }

    # 分析每个问题的答案对应的特质
    for question_id, answer_index in answers.items():
        question_id_int = int(question_id)
        answer_index_int = int(answer_index)

        # 根据映射关系增加特质分数
        if (
            question_id_int in answer_trait_mapping
            and answer_index_int in answer_trait_mapping[question_id_int]
        ):
            trait_mapping = answer_trait_mapping[question_id_int][answer_index_int]
            for dimension, trait in trait_mapping.items():
                if dimension in trait_scores and trait in trait_scores[dimension]:
                    trait_scores[dimension][trait] += 1

    # 计算每个维度的主要特质
    primary_traits = {}
    for dimension, traits in trait_scores.items():
        if traits:
            primary_trait = max(traits.items(), key=lambda x: x[1])
            primary_traits[dimension] = primary_trait[0]

    # 找出分数最高的两个特质维度
    dimension_scores = {}
    for dimension, traits in trait_scores.items():
        # 计算维度的总分（所有特质分数的平均值）
        total_score = sum(traits.values())
        avg_score = total_score / len(traits) if traits else 0
        dimension_scores[dimension] = avg_score

    # 按分数排序，取前两个
    top_dimensions = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)[
        :2
    ]
    top_primary_traits = {
        dim: primary_traits[dim]
        for dim, score in top_dimensions
        if dim in primary_traits
    }

    # 生成雷达图数据
    radar_data = generate_radar_data(trait_scores)

    return trait_scores, top_primary_traits, radar_data


def generate_radar_data(trait_scores):
    """生成雷达图数据"""
    # 计算每个维度的总分（标准化到0-100）
    dimensions = list(TRAIT_DIMENSIONS.keys())
    scores = []

    for dimension in dimensions:
        if dimension in trait_scores:
            traits = trait_scores[dimension]
            # 计算维度总分（所有特质分数的平均值）
            total_score = sum(traits.values())
            avg_score = total_score / len(traits) if traits else 0
            # 标准化到0-100（假设最大可能分数为5）
            normalized_score = min(avg_score * 20, 100)
            scores.append(int(normalized_score))
        else:
            scores.append(0)

    return {"dimensions": dimensions, "scores": scores, "max_score": 100}


@router.get("/questions", response_model=List[QuizQuestion])
async def get_quiz_questions():
    """获取所有答题题目"""
    return QUIZ_QUESTIONS


@router.post("/submit", response_model=Dict[str, Any])
async def submit_quiz(submission: QuizSubmission, db: AsyncSession = Depends(get_db)):
    """提交答题结果"""
    # 生成4位唯一代码
    unique_code = await generate_4_digit_code(db)

    # 分析个人特质
    trait_scores, top_primary_traits, radar_data = analyze_traits(submission.answers)

    # 创建数据库记录
    quiz_result = QuizResult(
        code=unique_code,
        participant_name=submission.participant_name,
        answers=submission.answers,
        trait_scores=trait_scores,
        primary_traits=top_primary_traits,
        radar_data=radar_data,
        submitted_at=datetime.now(),
    )

    # 保存到数据库
    db.add(quiz_result)
    await db.commit()
    await db.refresh(quiz_result)

    return {
        "unique_code": unique_code,
        "trait_scores": trait_scores,
        "primary_traits": top_primary_traits,
        "radar_data": radar_data,
        "message": f"答题完成！你的4位唯一代码是：{unique_code}，请记住这个代码用于特质匹配。",
    }


@router.post("/match", response_model=Dict[str, Any])
async def match_traits(code1: str, code2: str, db: AsyncSession = Depends(get_db)):
    """通过两个代码匹配特质"""
    # 从数据库查询代码1
    result1 = await db.execute(select(QuizResult).where(QuizResult.code == code1))
    submission1 = result1.scalar_one_or_none()
    if not submission1:
        raise HTTPException(status_code=404, detail=f"代码 {code1} 不存在")

    # 从数据库查询代码2
    result2 = await db.execute(select(QuizResult).where(QuizResult.code == code2))
    submission2 = result2.scalar_one_or_none()
    if not submission2:
        raise HTTPException(status_code=404, detail=f"代码 {code2} 不存在")

    # 计算特质匹配度
    compatibility_score = calculate_trait_compatibility(
        submission1.primary_traits, submission2.primary_traits
    )

    # 生成匹配分析
    match_analysis = generate_match_analysis(
        submission1.primary_traits, submission2.primary_traits
    )

    return {
        "code1": code1,
        "code2": code2,
        "participant1": submission1.participant_name or "匿名用户",
        "participant2": submission2.participant_name or "匿名用户",
        "compatibility_score": compatibility_score,
        "trait_scores1": submission1.trait_scores,
        "trait_scores2": submission2.trait_scores,
        "primary_traits1": submission1.primary_traits,
        "primary_traits2": submission2.primary_traits,
        "radar_data1": submission1.radar_data,
        "radar_data2": submission2.radar_data,
        "match_analysis": match_analysis,
        "message": f"特质匹配完成！匹配度为：{compatibility_score}%",
    }


def calculate_trait_compatibility(traits1, traits2):
    """计算特质匹配度"""
    if not traits1 or not traits2:
        return 0

    # 计算共同维度的匹配度
    common_dimensions = set(traits1.keys()) & set(traits2.keys())
    if not common_dimensions:
        return 0

    # 计算匹配度：相同特质得1分，不同特质得0.5分
    total_score = 0
    for dimension in common_dimensions:
        if traits1[dimension] == traits2[dimension]:
            total_score += 1
        else:
            total_score += 0.5

    # 转换为百分比
    compatibility = (total_score / len(common_dimensions)) * 100
    return int(compatibility)


def generate_match_analysis(traits1, traits2):
    """生成特质匹配分析"""
    analysis = []

    for dimension in traits1:
        if dimension in traits2:
            trait1 = traits1[dimension]
            trait2 = traits2[dimension]

            if trait1 == trait2:
                analysis.append(f"{dimension}：两人都是{trait1}，非常契合！")
            else:
                analysis.append(
                    f"{dimension}：一人是{trait1}，一人是{trait2}，可以互补"
                )

    return analysis


@router.get("/stats", response_model=Dict[str, Any])
async def get_quiz_stats(db: AsyncSession = Depends(get_db)):
    """获取答题统计信息"""
    # 从数据库查询所有答题记录
    result = await db.execute(select(QuizResult))
    all_submissions = result.scalars().all()

    if not all_submissions:
        raise HTTPException(status_code=404, detail="暂无答题记录")

    # 计算统计信息
    total_submissions = len(all_submissions)
    total_participants = len(
        set(s.participant_name for s in all_submissions if s.participant_name)
    )

    # 计算平均得分
    match_scores = []
    for submission in all_submissions:
        total_questions = len(submission.answers)
        if total_questions > 0:
            answer_patterns = {}
            for answer_index in submission.answers.values():
                answer_patterns[answer_index] = answer_patterns.get(answer_index, 0) + 1
            diversity_score = len(answer_patterns) / total_questions
            match_scores.append(int(diversity_score * 100))

    average_match_score = sum(match_scores) / len(match_scores) if match_scores else 0
    best_match_score = max(match_scores) if match_scores else 0

    # 计算排名
    match_rankings = {}
    if match_scores:
        sorted_scores = sorted(match_scores, reverse=True)
        for i, score in enumerate(sorted_scores[:10]):  # 只显示前10名
            match_rankings[f"第{i + 1}名"] = score

    last_submission = max(all_submissions, key=lambda x: x.submitted_at)

    return {
        "total_participants": total_participants,
        "total_submissions": total_submissions,
        "average_match_score": round(average_match_score, 2),
        "best_match_score": best_match_score,
        "last_submission_time": last_submission.submitted_at,
        "top_rankings": match_rankings,
    }


@router.get("/leaderboard", response_model=List[Dict[str, Any]])
async def get_leaderboard(db: AsyncSession = Depends(get_db)):
    """获取答题排行榜"""
    # 从数据库查询所有答题记录
    result = await db.execute(select(QuizResult))
    all_submissions = result.scalars().all()

    if not all_submissions:
        return []

    # 计算每个参与者的得分
    participant_scores = {}
    for submission in all_submissions:
        participant_name = submission.participant_name or "匿名用户"
        total_questions = len(submission.answers)

        if total_questions > 0:
            # 计算答案多样性得分
            answer_patterns = {}
            for answer_index in submission.answers.values():
                answer_patterns[answer_index] = answer_patterns.get(answer_index, 0) + 1
            diversity_score = len(answer_patterns) / total_questions
            match_score = int(diversity_score * 100)

            # 确定匹配等级
            if match_score >= 90:
                match_level = "非常了解"
                analysis = "对室友的了解非常全面！"
            elif match_score >= 70:
                match_level = "比较了解"
                analysis = "对室友有不错的了解！"
            elif match_score >= 50:
                match_level = "基本了解"
                analysis = "对室友有一定了解！"
            else:
                match_level = "需要更多了解"
                analysis = "还需要更多时间了解室友～"

            # 只保留每个参与者的最高分
            if (
                participant_name not in participant_scores
                or match_score > participant_scores[participant_name]["score"]
            ):
                participant_scores[participant_name] = {
                    "score": match_score,
                    "total_questions": total_questions,
                    "match_level": match_level,
                    "analysis": analysis,
                    "submitted_at": submission.submitted_at,
                }

    # 转换为排行榜结果
    leaderboard = []
    for participant_name, score_data in participant_scores.items():
        leaderboard.append(
            {
                "participant_name": participant_name,
                "match_score": score_data["score"],
                "total_questions": score_data["total_questions"],
                "match_level": score_data["match_level"],
                "analysis": score_data["analysis"],
                "submitted_at": score_data["submitted_at"],
            }
        )

    # 按得分排序并设置排名
    leaderboard.sort(key=lambda x: x["match_score"], reverse=True)
    for i, result in enumerate(leaderboard):
        result["rank"] = i + 1

    return leaderboard


@router.get("/verify/{code}")
async def verify_quiz_code(code: str, db: AsyncSession = Depends(get_db)):
    """验证答题唯一代码"""
    # 从数据库查询代码
    result = await db.execute(select(QuizResult).where(QuizResult.code == code))
    submission = result.scalar_one_or_none()

    if not submission:
        raise HTTPException(status_code=404, detail="无效的代码")

    # 计算得分
    total_questions = len(submission.answers)
    if total_questions > 0:
        answer_patterns = {}
        for answer_index in submission.answers.values():
            answer_patterns[answer_index] = answer_patterns.get(answer_index, 0) + 1
        diversity_score = len(answer_patterns) / total_questions
        match_score = int(diversity_score * 100)
    else:
        match_score = 0

    return {
        "code_valid": True,
        "participant_name": submission.participant_name or "匿名用户",
        "match_score": match_score,
        "total_questions": total_questions,
        "trait_scores": submission.trait_scores,
        "primary_traits": submission.primary_traits,
        "radar_data": submission.radar_data,
        "generated_at": submission.submitted_at,
        "message": "代码验证成功",
    }
