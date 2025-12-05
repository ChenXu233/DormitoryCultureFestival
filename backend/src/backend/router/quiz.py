from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from datetime import datetime
import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..schema.quiz import (
    QuizQuestion,
    QuizSubmission,
    MatchResult,
    TeamMatchRequest,
    TeamMatchResult,
)
from ..model.quiz import QuizResult
from ..database import async_session

router = APIRouter(prefix="/quiz", tags=["答题模块"])

# 特质维度定义（根据MD文件中的对应维度）
TRAIT_DIMENSIONS = {
    "生活习惯": ["秩序执政官", "灵活适应者", "规律执行者", "随性自由者"],
    "社交倾向": ["氛围感应炉", "外向活跃者", "内向安静者", "平衡调节者"],
    "作息规律": ["生物钟协调员", "早睡早起者", "夜猫子", "弹性作息者"],
    "学习风格": ["知识催化剂", "独立学习者", "小组学习者", "多元学习者"],
    "娱乐偏好": ["快乐能量站", "安静活动者", "户外活动者", "社交活动者"],
    "饮食习惯": ["味蕾合伙人", "健康饮食者", "美食探索者", "简单饮食者"],
    "卫生习惯": ["空间美化师", "高度整洁者", "适度整洁者", "舒适导向者"],
    "沟通方式": ["信号中继器", "直接沟通者", "委婉沟通者", "行动沟通者"],
}

# 特质维度 Emoji 映射
TRAIT_EMOJIS = {
    "生活习惯": "🛏️",
    "社交倾向": "👥",
    "作息规律": "⏰",
    "学习风格": "📚",
    "娱乐偏好": "🎮",
    "饮食习惯": "🍽️",
    "卫生习惯": "🚿",
    "沟通方式": "💬",
}

# 题库数据 - 每个选项包含对预设特质的加分项（趣味化问卷风格）
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "周末生存指南：你的首选模式是？",
        "options": [
            "A. 寝室宅神：床是我永远的恋人与战场，休息充电才是正经事。",
            "B. 社交牛人：呼朋引伴，组局逛街干饭，电量在人群中满格！",
            "C. 卷王出动：图书馆、自习室是我的主舞台，学业/事业才是周末的归宿。",
            "D. 户外达人：拥抱自然，骑行爬山，用运动唤醒多巴胺。",
        ],
        "traits": ["生活习惯", "社交倾向", "娱乐偏好"],
        "option_scores": [
            {"生活习惯": {"规律执行者": 2}, "娱乐偏好": {"安静活动者": 2}},
            {
                "生活习惯": {"灵活适应者": 2},
                "社交倾向": {"外向活跃者": 2},
                "娱乐偏好": {"社交活动者": 1},
            },
            {"生活习惯": {"规律执行者": 1}, "学习风格": {"独立学习者": 2}},
            {"生活习惯": {"灵活适应者": 1}, "娱乐偏好": {"户外活动者": 2}},
        ],
    },
    {
        "id": 2,
        "question": "期末破防时，你的复习姿势是？",
        "options": [
            "A. 孤独的王者：习惯单打独斗，一壶水一本书，一个人就是一支队伍。",
            "B. 讨论区战神：必须和小伙伴一起，互相提问答疑，知识在碰撞中巩固。",
            "C. BGM 爱好者：耳机一戴，谁都不爱，白噪音或音乐是专注的必备 BGM。",
            "D. 绝对安静派：需要图书馆级别的静音环境，一点声响都会破功。",
        ],
        "traits": ["学习风格", "生活习惯"],
        "option_scores": [
            {"学习风格": {"独立学习者": 2}, "生活习惯": {"规律执行者": 1}},
            {"学习风格": {"小组学习者": 2}, "社交倾向": {"外向活跃者": 1}},
            {"学习风格": {"多元学习者": 2}, "生活习惯": {"灵活适应者": 1}},
            {"学习风格": {"独立学习者": 2}, "生活习惯": {"规律执行者": 1}},
        ],
    },
    {
        "id": 3,
        "question": "你的书桌/床位通常是什么画风？",
        "options": [
            "A. 样板间风格：物品各归其位，随手整理，强迫症感到极度舒适。",
            "B. 周期性整洁：偶尔会看不下去，然后进行一次高效的大扫除。",
            "C. 周末仪式感：将大扫除作为一周的结束和新一周的开始。",
            'D. 凌乱美学派："乱中有序"是我的哲学，别动，我能找到任何东西！',
        ],
        "traits": ["卫生习惯", "生活习惯"],
        "option_scores": [
            {"卫生习惯": {"高度整洁者": 3}, "生活习惯": {"规律执行者": 2}},
            {"卫生习惯": {"适度整洁者": 2}, "生活习惯": {"规律执行者": 1}},
            {"卫生习惯": {"适度整洁者": 1}, "生活习惯": {"灵活适应者": 1}},
            {"卫生习惯": {"舒适导向者": 2}, "生活习惯": {"灵活适应者": 2}},
        ],
    },
    {
        "id": 4,
        "question": '你的"社交电量"通常如何消耗？',
        "options": [
            "A. 能量爆棚：热衷大型聚会和集体活动，人越多越嗨。",
            "B. 精准放电：偏爱三五知己的小范围深度聊天，质量高于数量。",
            "C. 节能模式：享受一对一的交流，更能建立深厚的情感连接。",
            'D. 线上王者：线上侃侃而谈，线下可能"电量不足"，擅长文字交流。',
        ],
        "traits": ["社交倾向", "沟通方式"],
        "option_scores": [
            {"社交倾向": {"外向活跃者": 3}, "沟通方式": {"直接沟通者": 1}},
            {"社交倾向": {"平衡调节者": 2}, "沟通方式": {"委婉沟通者": 1}},
            {"社交倾向": {"内向安静者": 2}, "沟通方式": {"委婉沟通者": 2}},
            {"社交倾向": {"氛围感应炉": 2}, "沟通方式": {"信号中继器": 2}},
        ],
    },
    {
        "id": 5,
        "question": "深夜寝室里，你通常属于哪一派？",
        "options": [
            'A. 养生先锋：秉承"美容觉"原则，熄灯就睡，迎接清晨的太阳。',
            "B. 标准作息：跟随学校的作息时间表，规律作息，健康生活。",
            "C. 弹性作息：根据当天任务灵活调整，偶尔熬夜，但尽量不死磕。",
            "D. 夜猫子本猫：灵感总在深夜爆发，夜晚是我精神的巅峰时段。",
        ],
        "traits": ["作息规律", "生活习惯"],
        "option_scores": [
            {"作息规律": {"早睡早起者": 3}, "生活习惯": {"规律执行者": 2}},
            {"作息规律": {"生物钟协调员": 2}, "生活习惯": {"规律执行者": 2}},
            {"作息规律": {"弹性作息者": 2}, "生活习惯": {"灵活适应者": 2}},
            {"作息规律": {"夜猫子": 3}, "生活习惯": {"灵活适应者": 2}},
        ],
    },
    {
        "id": 6,
        "question": "食堂/外卖抉择时，你最看重啥？",
        "options": [
            "A. 健康卫士：营养均衡是首位，轻食沙拉常在我的菜单。",
            "B. 味蕾探险家：味道至上，愿意为了一口好吃的穿越整个校园。",
            "C. 极简主义者：方便快捷最重要，能填饱肚子且不耽误时间就行。",
            "D. 性价比之王：精打细算，用最少的钱获得最大的满足感。",
        ],
        "traits": ["饮食习惯", "生活习惯"],
        "option_scores": [
            {"饮食习惯": {"健康饮食者": 3}, "生活习惯": {"规律执行者": 1}},
            {"饮食习惯": {"美食探索者": 2}, "生活习惯": {"灵活适应者": 1}},
            {"饮食习惯": {"简单饮食者": 2}, "生活习惯": {"灵活适应者": 1}},
            {"饮食习惯": {"味蕾合伙人": 2}, "生活习惯": {"灵活适应者": 1}},
        ],
    },
    {
        "id": 7,
        "question": "小组作业出现分歧，你的第一反应是？",
        "options": [
            "A. 直球选手：直接提出自己的想法和疑虑，高效沟通解决问题。",
            'B. 委婉大师：会先肯定对方，再用"我们是不是可以…"的方式建议。',
            "C. 文档高手：倾向于先整理好自己的思路和论据，用文档说话。",
            "D. 观察行动派：不急于表态，先观察局势，再用行动示范自己的方案。",
        ],
        "traits": ["沟通方式", "学习风格"],
        "option_scores": [
            {"沟通方式": {"直接沟通者": 3}, "社交倾向": {"外向活跃者": 1}},
            {"沟通方式": {"委婉沟通者": 3}, "社交倾向": {"平衡调节者": 1}},
            {"沟通方式": {"信号中继器": 2}, "学习风格": {"知识催化剂": 2}},
            {"沟通方式": {"行动沟通者": 2}, "学习风格": {"独立学习者": 2}},
        ],
    },
    {
        "id": 8,
        "question": '经历"满课地狱"后，你如何快速回血？',
        "options": [
            "A. 静态恢复：戴上耳机听歌，或看一本闲书，让世界安静下来。",
            "B. 动态解压：去操场跑几圈或者健身房出出汗，挥洒汗水解千愁。",
            "C. 话疗专家：找室友或好友疯狂输出、大吐苦水，说完就好了。",
            "D. 虚拟世界：开局游戏或刷部剧，瞬间沉浸，烦恼全抛在脑后。",
        ],
        "traits": ["娱乐偏好", "社交倾向"],
        "option_scores": [
            {"娱乐偏好": {"安静活动者": 3}, "社交倾向": {"内向安静者": 1}},
            {"娱乐偏好": {"户外活动者": 2}, "社交倾向": {"外向活跃者": 2}},
            {"娱乐偏好": {"社交活动者": 3}, "社交倾向": {"外向活跃者": 2}},
            {"娱乐偏好": {"快乐能量站": 2}, "学习风格": {"知识催化剂": 1}},
        ],
    },
    {
        "id": 9,
        "question": '你对寝室个人"领地"的整洁度有多执着？',
        "options": [
            "A. 洁癖担当：无法容忍任何灰尘，桌面和床铺必须时刻整洁如新。",
            "B. 整洁维护者：会定期收拾，保持一个看得过去的整洁环境。",
            "C. 舒适导向：东西可以多，但不能脏，乱一点但有自己秩序也很舒服。",
            "D. 自由灵魂：追求精神世界的富足，对外在环境整洁度要求不高。",
        ],
        "traits": ["卫生习惯", "生活习惯"],
        "option_scores": [
            {"卫生习惯": {"高度整洁者": 3}, "生活习惯": {"规律执行者": 2}},
            {"卫生习惯": {"适度整洁者": 2}, "生活习惯": {"规律执行者": 1}},
            {"卫生习惯": {"适度整洁者": 1}, "生活习惯": {"灵活适应者": 1}},
            {"卫生习惯": {"舒适导向者": 2}, "生活习惯": {"灵活适应者": 2}},
        ],
    },
    {
        "id": 10,
        "question": '你理想中的"完美自习室"是？',
        "options": [
            "A. 图书馆：鸦雀无声，连翻书声都显得刺耳，绝对安静才能专注。",
            "B. 白噪音舱：需要有一些背景音，比如图书馆的轻微嘈杂或轻音乐。",
            "C. 研讨间：喜欢和同学一起学习，可以随时低声交流、互相启发。",
            "D. 露天咖啡馆：喜欢在通风、有自然光的环境下学习，比如室外或窗边。",
        ],
        "traits": ["学习风格", "娱乐偏好"],
        "option_scores": [
            {"学习风格": {"独立学习者": 3}, "社交倾向": {"内向安静者": 1}},
            {"学习风格": {"多元学习者": 2}, "生活习惯": {"灵活适应者": 1}},
            {"学习风格": {"小组学习者": 2}, "社交倾向": {"外向活跃者": 2}},
            {"学习风格": {"知识催化剂": 2}, "娱乐偏好": {"户外活动者": 1}},
        ],
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
    """分析答题结果，推断个人特质并计算分数（基于每个选项的加分表）"""
    # 初始化特质分数
    trait_scores = {
        dimension: {trait: 0 for trait in traits}
        for dimension, traits in TRAIT_DIMENSIONS.items()
    }

    # 构建快速查找：问题ID -> option_scores 列表
    question_score_map = {q["id"]: q.get("option_scores", []) for q in QUIZ_QUESTIONS}

    # 累加每个选项给到的分数
    for question_id, answer_index in answers.items():
        try:
            qid = int(question_id)
            idx = int(answer_index)
        except Exception:
            continue

        option_scores = question_score_map.get(qid)
        if not option_scores or idx < 0 or idx >= len(option_scores):
            continue

        score_map = option_scores[idx]
        # score_map: {dimension: {trait: points, ...}, ...}
        for dimension, trait_map in score_map.items():
            if dimension not in trait_scores:
                # 忽略未注册的维度
                continue
            for trait, points in trait_map.items():
                if trait in trait_scores[dimension]:
                    try:
                        trait_scores[dimension][trait] += int(points)
                    except Exception:
                        # 忽略非整数分值
                        continue

    # 计算每个维度的主要特质
    primary_traits = {}
    for dimension, traits in trait_scores.items():
        if traits:
            primary_trait = max(traits.items(), key=lambda x: x[1])
            primary_traits[dimension] = primary_trait[0]

    # 找出分数最高的两个特质维度（按维度平均分）
    dimension_scores = {}
    for dimension, traits in trait_scores.items():
        total_score = sum(traits.values())
        avg_score = total_score / len(traits) if traits else 0
        dimension_scores[dimension] = avg_score

    top_dimensions = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)[
        :2
    ]
    top_primary_traits = {
        dim: primary_traits[dim]
        for dim, score in top_dimensions
        if dim in primary_traits
    }

    # 生成雷达图数据（使用每个维度的得分相对于该维度可能的最高分进行标准化）
    radar_data = generate_radar_data(trait_scores)

    return trait_scores, top_primary_traits, radar_data


def generate_radar_data(trait_scores):
    """生成雷达图数据"""
    dimensions = list(TRAIT_DIMENSIONS.keys())
    scores = []

    # 计算每个维度可能的最大总分（基于问卷中各题的最大加分）
    max_possible_by_dimension = {dim: 0 for dim in dimensions}
    for q in QUIZ_QUESTIONS:
        opt_scores = q.get("option_scores", [])
        # 对于该题每个维度，取该题中所有选项在该维度上给予的最大分
        per_question_max = {}
        for opt in opt_scores:
            for dim, trait_map in opt.items():
                per_question_max[dim] = max(
                    per_question_max.get(dim, 0),
                    sum(
                        int(v)
                        for v in trait_map.values()
                        if isinstance(v, (int, float))
                    ),
                )

        for dim, val in per_question_max.items():
            if dim in max_possible_by_dimension:
                max_possible_by_dimension[dim] += val

    # 现在根据实际得分与可能最高分来标准化到0-100
    for dimension in dimensions:
        traits = trait_scores.get(dimension, {})
        total_score = sum(traits.values())
        max_possible = max_possible_by_dimension.get(dimension, 0)
        if max_possible > 0:
            normalized = int(min(100, (total_score / max_possible) * 100))
        else:
            normalized = 0
        scores.append(normalized)

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

    # 返回给前端的数据，包含前端页面预期的字段名
    # 前端 `quiz.vue` 期望 `unique_code`, `message`, `traits` (主要特质) 以及 `trait_scores` 和 `radar_data`
    response_payload = {
        "unique_code": unique_code,
        "trait_scores": trait_scores,
        "primary_traits": top_primary_traits,
        "traits": top_primary_traits,
        "radar_data": radar_data,
        "dimension_emojis": TRAIT_EMOJIS,
        "message": f"答题完成！你的唯一代码是：{unique_code}，请记住这个代码用于特质匹配。",
    }

    # 尝试从提交数据中计算用时（如果前端上传了 submitted_at）
    try:
        if submission.submitted_at:
            # submitted_at 由前端传入，可能为 datetime 或字符串（pydantic 已解析为 datetime）
            time_spent_seconds = int(
                (datetime.now() - submission.submitted_at).total_seconds()
            )
            # 不强求准确，这只是一个可选字段，前端也会本地计算并覆盖
            response_payload["time_spent"] = max(time_spent_seconds, 0)
    except Exception:
        # 忽略计算错误，不影响主要流程
        response_payload["time_spent"] = 0

    return response_payload


@router.post("/match", response_model=Dict[str, Any])
async def match_traits(request: Dict[str, Any], db: AsyncSession = Depends(get_db)):
    code1 = request.get("code1")
    code2 = request.get("code2")
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

    # 返回前端期望的数据结构
    return {
        "compatibility_score": compatibility_score,
        "match_analysis": match_analysis,
        "traits1": submission1.primary_traits,
        "traits2": submission2.primary_traits,
        "participant1_name": submission1.participant_name or "匿名用户",
        "participant2_name": submission2.participant_name or "匿名用户",
        "dimension_emojis": TRAIT_EMOJIS,
        # 保留其他数据供可能的使用
        "code1": code1,
        "code2": code2,
        "trait_scores1": submission1.trait_scores,
        "trait_scores2": submission2.trait_scores,
        "primary_traits1": submission1.primary_traits,
        "primary_traits2": submission2.primary_traits,
        "radar_data1": submission1.radar_data,
        "radar_data2": submission2.radar_data,
        "message": f"特质匹配完成！匹配度为：{compatibility_score}%",
    }


@router.post("/team-match", response_model=Dict[str, Any])
async def match_team_traits(
    request: Dict[str, Any], db: AsyncSession = Depends(get_db)
):
    """四人团队特质匹配"""
    codes = request.get("codes", [])

    if len(codes) != 4:
        raise HTTPException(status_code=400, detail="请提供4个有效的代码")

    # 从数据库查询所有四个代码对应的答题结果
    submissions = []
    for code in codes:
        result = await db.execute(select(QuizResult).where(QuizResult.code == code))
        submission = result.scalar_one_or_none()
        if not submission:
            raise HTTPException(status_code=404, detail=f"代码 {code} 不存在")
        submissions.append(submission)

    # 计算团队特质匹配度
    team_compatibility_score = calculate_team_compatibility(submissions)

    # 分析团队特质分布
    team_trait_analysis = analyze_team_traits(submissions)

    # 生成团队评语（基于团队中特定特质最多的人）
    team_commentary = generate_team_commentary(team_trait_analysis)

    # 返回团队匹配结果
    return {
        "team_compatibility_score": team_compatibility_score,
        "team_trait_analysis": team_trait_analysis,
        "team_commentary": team_commentary,
        "dimension_emojis": TRAIT_EMOJIS,
        "participants": [
            {
                "code": submission.code,
                "name": submission.participant_name or "匿名用户",
                "primary_traits": submission.primary_traits,
                "trait_scores": submission.trait_scores,
                "radar_data": submission.radar_data,
            }
            for submission in submissions
        ],
        "message": f"四人团队特质匹配完成！团队匹配度为：{team_compatibility_score}%",
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


def calculate_team_compatibility(submissions):
    """计算四人团队的特质匹配度"""
    if len(submissions) != 4:
        return 0

    # 计算所有两两组合的匹配度
    total_compatibility = 0
    pair_count = 0

    for i in range(4):
        for j in range(i + 1, 4):
            compatibility = calculate_trait_compatibility(
                submissions[i].primary_traits, submissions[j].primary_traits
            )
            total_compatibility += compatibility
            pair_count += 1

    # 计算平均匹配度
    if pair_count > 0:
        return int(total_compatibility / pair_count)
    return 0


def analyze_team_traits(submissions):
    """分析团队特质分布"""
    if len(submissions) != 4:
        return {}

    # 统计每个维度中各种特质的出现次数
    trait_distribution = {}

    for submission in submissions:
        for dimension, trait in submission.primary_traits.items():
            if dimension not in trait_distribution:
                trait_distribution[dimension] = {}

            if trait not in trait_distribution[dimension]:
                trait_distribution[dimension][trait] = 0
            trait_distribution[dimension][trait] += 1

    # 找出每个维度中最常见的特质
    dominant_traits = {}
    for dimension, traits in trait_distribution.items():
        if traits:
            dominant_trait = max(traits.items(), key=lambda x: x[1])
            dominant_traits[dimension] = {
                "trait": dominant_trait[0],
                "count": dominant_trait[1],
                "percentage": int((dominant_trait[1] / 4) * 100),
            }

    # 找出团队中最突出的特质维度（出现次数最多的特质）
    most_common_trait_info = None
    for dimension, info in dominant_traits.items():
        if (
            not most_common_trait_info
            or info["count"] > most_common_trait_info["count"]
        ):
            most_common_trait_info = {
                "dimension": dimension,
                "trait": info["trait"],
                "count": info["count"],
                "percentage": info["percentage"],
            }

    return {
        "trait_distribution": trait_distribution,
        "dominant_traits": dominant_traits,
        "most_common_trait": most_common_trait_info,
    }


def generate_team_commentary(team_trait_analysis):
    """生成团队评语，基于团队特质分布和匹配度设计文档"""
    if not team_trait_analysis or not team_trait_analysis.get("dominant_traits"):
        return {
            "title": "多元融合团队",
            "commentary": "你们的团队特质分布均衡，每个人都有自己的特色，能够形成良好的互补关系。",
            "type": "平衡型",
        }

    dominant_traits = team_trait_analysis.get("dominant_traits", {})
    
    # 单维度称号定义（对应设计文档中的单一维度）
    single_dimension_titles = {
        "生活习惯": ("秩序议会", "本寝以'法度'严明著称，物品归位、作息稳定，一切行动皆有章法，宛如一个高效运转的小小议会。"),
        "社交倾向": ("情报交换中心", "这里是校园信息的集散地，既能安静内敛，也能热烈开放，总能源源不断地输出各种趣闻与动态。"),
        "作息规律": ("生物钟协调局", "你们深谙睡眠的奥义，无论是早睡早起还是夜猫子，都能相互理解并找到和谐的共存节奏，是寝室的时间管理大师。"),
        "学习风格": ("深度学习俱乐部", "无论是独自钻研还是小组碰撞，这里总能激发学习动力，是寝室成员共同进步、互为'学伴'的智慧空间。"),
        "娱乐偏好": ("快乐能量站", "你们是寝室活力的源泉，总能策划出最有趣的放松活动，让小小的空间充满欢声笑语，快速驱散学习的疲惫。"),
        "饮食习惯": ("味蕾合伙人", "你们是彼此最可靠的'饭搭子'，不仅能吃在一起，更能理解对方的口味偏好，是共享美味、分担烦恼的黄金搭档。"),
        "卫生习惯": ("五星级样板间", "本寝以环境整洁闻名，对生活品质有共同的高要求，共同维护着令人心安的整洁与有序，堪称寝室楼的卫生标杆。"),
        "沟通方式": ("联合国调解庭", "成员间沟通顺畅高效，善于表达也能倾听，能妥善协调内部'事务'，是寝室和谐共处的关键。"),
    }
    
    # 维度组合称号定义（对应设计文档中的组合维度）
    combination_titles = {
        ("生活习惯", "社交倾向"): ("自律者联盟", "既能打理好井井有条的个人生活，又能在社交场合中游刃有余，你们在自律与开放间找到了完美的平衡点。"),
        ("生活习惯", "作息规律"): ("永动时钟塔", "你们将生活规律与作息节奏深度融合，形成了一种稳定而可持续的日常模式，让寝室如同一个高效且温馨的生态系统。"),
        ("生活习惯", "学习风格"): ("高效能研究所", "良好的生活习惯为学习奠定了坚实基础，让你们能在专注投入后获得扎实的收获，是厚积薄发的典范。"),
        ("生活习惯", "娱乐偏好"): ("品质生活馆", "你们懂得张弛有道，既能认真生活，也精通如何放松，善于从日常和娱乐中发现并创造高品质的乐趣。"),
        ("生活习惯", "饮食习惯"): ("日常仪式部", "你们将规律的饮食融入生活哲学，即使是简单的一日三餐，也能被你们经营出满满的仪式感和幸福感。"),
        ("生活习惯", "卫生习惯"): ("公约守护者", "对生活品质和环境卫生有着共同的高要求，彼此理解并共同维护着那份令人心安的整洁与有序。"),
        ("生活习惯", "沟通方式"): ("公约制定局", "善于将生活习惯转化为清晰的沟通语言，能有效地制定、解释并协同执行寝室的各项'公约'，是制度的良好维护者。"),
        ("社交倾向", "作息规律"): ("能量调度中心", "能根据彼此的作息能量状态，灵活安排社交互动，既尊重休息时间，也能在共同活跃时充分享受交流的快乐。"),
        ("社交倾向", "学习风格"): ("学术社交圈", "在学习与社交间架起桥梁，能组建高效的学习小组，也能在知识分享中增进友谊，实现1+1>2的共赢。"),
        ("社交倾向", "娱乐偏好"): ("派对引擎", "你们是集体欢乐的制造核心，总能点燃气氛，策划出令人难忘的娱乐活动，是当之无愧的寝室气氛担当。"),
        ("社交倾向", "饮食习惯"): ("美食雷达", "对美食有着共同的热情和敏锐的嗅觉，不仅是彼此的'饭搭子'，更是探索城市美味地图的最佳拍档。"),
        ("社交倾向", "卫生习惯"): ("温馨共建委", "既注重公共环境的整洁，也乐于通过共同劳动（如大扫除）来增进社交互动，是寝室温暖的共同营造者。"),
        ("社交倾向", "沟通方式"): ("频道同步组", "沟通方式与社交频率高度同频，总能迅速理解对方的点，交流起来毫不费力，是彼此最佳的倾诉和倾听对象。"),
        ("作息规律", "学习风格"): ("时间规划局", "能将作息规律与学习高峰期完美结合，制定出最科学高效的日程表，是时间管理领域的资深专家。"),
        ("作息规律", "娱乐偏好"): ("续航管理办", "懂得如何通过娱乐来为身心充电，也能在尽情玩耍后迅速回归休息状态，是精力管理的优等生。"),
        ("作息规律", "饮食习惯"): ("养生联盟", "深谙'食饮有节，起居有常'之道，将规律的饮食和作息结合，是寝室里的健康生活实践派。"),
        ("作息规律", "卫生习惯"): ("晨型清洁组", "或许是在清晨或夜晚，总能默契地共同维护寝室整洁，在安静中完成打扫，互不打扰又彼此支持。"),
        ("作息规律", "沟通方式"): ("静音协议厅", "深刻理解并尊重彼此的作息时间，能在需要安静时自动切换沟通模式（如使用文字），是体贴的模范。"),
        ("学习风格", "娱乐偏好"): ("劳逸平衡会", "坚信'学就学个踏实，玩就玩个痛快'，能在两种模式间无缝切换，是寝室里最懂得平衡之道的生活家。"),
        ("学习风格", "饮食习惯"): ("脑力加油站", "深知美食对学习的重要性，能在挑灯夜战或完成报告后，用恰到好处的美味互相慰藉，补充脑力。"),
        ("学习风格", "卫生习惯"): ("灵感交换站", "注重学习环境的整洁，并认为清晰的物理空间有助于激发清晰的思维，是思想与空间共同进化的代表。"),
        ("学习风格", "沟通方式"): ("知识交换所", "乐于并善于分享学习心得和方法，通过有效的沟通碰撞出思维的火花，是彼此学业上最佳的益友。"),
        ("娱乐偏好", "饮食习惯"): ("享乐理事会", "最懂如何将娱乐与美食结合，达到快乐最大值，是策划寝室观影聚餐等活动的金牌策划师。"),
        ("娱乐偏好", "卫生习惯"): ("玩趣保洁团", "即便在尽情娱乐后，也能默契地快速恢复环境整洁，做到了'欢乐留心底，场地速清理'。"),
        ("娱乐偏好", "沟通方式"): ("梗文化研究", "你们创造的内部梗和笑点是寝室的独特文化，沟通方式本身就成了一种极富乐趣的娱乐活动。"),
        ("饮食习惯", "卫生习惯"): ("美味品鉴社", "既享受美食带来的愉悦，也共同注重用餐后的环境整理，对美味的追求与对整洁的维护在你们身上和谐统一。"),
        ("饮食习惯", "沟通方式"): ("餐桌议事厅", "饭桌是你们最好的交流场所，许多重要决策和深度谈话，都在分享美食的过程中轻松达成。"),
        ("卫生习惯", "沟通方式"): ("空间协调组", "能通过友好沟通妥善解决卫生分工等公共空间问题，是寝室公共区域和谐的基石。"),
    }
    
    # 找出得分最高的前两个维度
    sorted_dimensions = sorted(
        dominant_traits.items(),
        key=lambda x: x[1]["percentage"],
        reverse=True
    )
    
    if len(sorted_dimensions) == 0:
        return {
            "title": "多元融合团队",
            "commentary": "你们的团队特质分布均衡，每个人都有自己的特色，能够形成良好的互补关系。",
            "type": "平衡型",
        }
    
    # 如果只有一个维度或第一个维度得分远高于第二个（差距>=25%），使用单维度称号
    if len(sorted_dimensions) == 1 or sorted_dimensions[0][1]["percentage"] - sorted_dimensions[1][1]["percentage"] >= 25:
        top_dimension = sorted_dimensions[0][0]
        title, commentary = single_dimension_titles.get(
            top_dimension,
            ("特质主导团队", f"你们的团队在{top_dimension}方面表现出色，形成了独特的寝室文化。")
        )
        return {
            "title": title,
            "commentary": commentary,
            "type": "单维度主导型",
            "dominant_dimension": top_dimension,
            "dominant_percentage": sorted_dimensions[0][1]["percentage"],
        }
    
    # 使用组合维度称号
    dim1 = sorted_dimensions[0][0]
    dim2 = sorted_dimensions[1][0]
    
    # 尝试两种顺序的组合
    title, commentary = (
        combination_titles.get((dim1, dim2)) or 
        combination_titles.get((dim2, dim1)) or
        ("多元协调团队", f"你们在{dim1}和{dim2}方面都表现突出，形成了独特的组合优势。")
    )
    
    return {
        "title": title,
        "commentary": commentary,
        "type": "组合优势型",
        "dimension1": dim1,
        "dimension2": dim2,
        "percentage1": sorted_dimensions[0][1]["percentage"],
        "percentage2": sorted_dimensions[1][1]["percentage"],
    }


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
