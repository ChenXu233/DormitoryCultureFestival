from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
import random
from ..schema.quiz import QuizQuestion, QuizSubmission, MatchResult, DormitoryMatchStats

router = APIRouter(prefix="/quiz", tags=["答题模块"])

# 模拟题库数据（无正确答案，用于测试室友之间的了解程度）
QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "你的室友最喜欢的食物是什么？",
        "options": ["火锅", "烧烤", "日料", "家常菜"],
        "category": "饮食习惯",
    },
    {
        "id": 2,
        "question": "你的室友通常几点睡觉？",
        "options": ["22:00前", "22:00-24:00", "24:00-2:00", "2:00后"],
        "category": "作息习惯",
    },
    {
        "id": 3,
        "question": "你的室友最喜欢的娱乐活动是什么？",
        "options": ["打游戏", "看电影", "运动", "看书"],
        "category": "兴趣爱好",
    },
    {
        "id": 4,
        "question": "你的室友最讨厌的事情是什么？",
        "options": ["噪音", "脏乱", "借东西不还", "不守时"],
        "category": "生活习惯",
    },
    {
        "id": 5,
        "question": "你的室友最喜欢的季节是？",
        "options": ["春天", "夏天", "秋天", "冬天"],
        "category": "个人偏好",
    },
    {
        "id": 6,
        "question": "你的室友最擅长的科目是什么？",
        "options": ["数学", "英语", "专业课", "体育"],
        "category": "学习能力",
    },
    {
        "id": 7,
        "question": "你的室友最喜欢的颜色是？",
        "options": ["蓝色", "红色", "绿色", "黑色"],
        "category": "个人偏好",
    },
    {
        "id": 8,
        "question": "你的室友最喜欢的音乐类型是？",
        "options": ["流行", "摇滚", "古典", "民谣"],
        "category": "兴趣爱好",
    },
    {
        "id": 9,
        "question": "你的室友最想去旅游的地方是？",
        "options": ["海边", "山区", "城市", "乡村"],
        "category": "旅行偏好",
    },
    {
        "id": 10,
        "question": "你的室友最喜欢的电影类型是？",
        "options": ["动作片", "喜剧片", "爱情片", "科幻片"],
        "category": "娱乐偏好",
    },
]

# 模拟存储答题记录
quiz_submissions = []


@router.get("/questions", response_model=List[QuizQuestion])
async def get_quiz_questions(count: int = 5):
    """获取答题问题列表"""
    if count > len(QUIZ_QUESTIONS):
        count = len(QUIZ_QUESTIONS)

    # 随机选择题目
    selected_questions = random.sample(QUIZ_QUESTIONS, count)
    return [QuizQuestion(**q) for q in selected_questions]


@router.post("/submit", response_model=MatchResult)
async def submit_quiz(submission: QuizSubmission):
    """提交答题结果，计算室友匹配度"""
    # 保存提交记录
    quiz_submissions.append(submission)

    # 计算匹配度：找到同一寝室、同一答题对象的其他提交记录进行对比
    matched_count = 0
    total_questions = len(submission.answers)

    # 查找同一寝室、同一答题对象的其他提交记录
    roommate_submissions = [
        sub
        for sub in quiz_submissions
        if (
            sub.dormitory_id == submission.dormitory_id
            and sub.target_roommate == submission.participant_name
            and sub.participant_name == submission.target_roommate
        )
    ]

    # 如果有对应的室友答题记录，计算匹配度
    if roommate_submissions:
        roommate_submission = roommate_submissions[0]
        for question_id, answer_index in submission.answers.items():
            if question_id in roommate_submission.answers:
                if answer_index == roommate_submission.answers[question_id]:
                    matched_count += 1

    # 计算匹配度分数
    match_percentage = matched_count / total_questions if total_questions > 0 else 0
    match_score = int(match_percentage * 100)

    # 确定匹配等级
    if match_percentage >= 0.8:
        match_level = "心灵相通"
    elif match_percentage >= 0.6:
        match_level = "默契十足"
    elif match_percentage >= 0.4:
        match_level = "互相了解"
    else:
        match_level = "还需磨合"

    # 生成匹配度分析
    insights = []
    if match_percentage >= 0.8:
        insights = ["你们对彼此非常了解！", "生活习惯高度一致", "兴趣爱好完美契合"]
    elif match_percentage >= 0.6:
        insights = [
            "你们相处得很不错",
            "大部分习惯都能互相理解",
            "继续加深了解会更默契",
        ]
    elif match_percentage >= 0.4:
        insights = [
            "你们对彼此有一定了解",
            "有些方面还需要更多沟通",
            "多交流能增进默契",
        ]
    else:
        insights = [
            "你们还需要更多时间相处",
            "多聊天了解对方的喜好",
            "共同活动能增进感情",
        ]

    # 计算排名（基于匹配度分数）
    all_match_scores = []
    for sub in quiz_submissions:
        if sub.dormitory_id == submission.dormitory_id:
            # 简化计算：这里假设每个提交都有对应的匹配记录
            all_match_scores.append(match_score)

    ranking = None
    if all_match_scores:
        sorted_scores = sorted(all_match_scores, reverse=True)
        ranking = sorted_scores.index(match_score) + 1

    result = MatchResult(
        match_score=match_score,
        total_questions=total_questions,
        matched_answers=matched_count,
        match_percentage=match_percentage,
        time_spent=300,  # 默认5分钟
        ranking=ranking,
        match_level=match_level,
        insights=insights,
    )

    return result


@router.get("/stats/{dormitory_id}", response_model=DormitoryMatchStats)
async def get_dormitory_stats(dormitory_id: str):
    """获取寝室匹配度统计"""
    dorm_submissions = [s for s in quiz_submissions if s.dormitory_id == dormitory_id]

    if not dorm_submissions:
        raise HTTPException(status_code=404, detail="未找到该寝室的答题记录")

    # 计算统计信息
    total_participants = len(set(s.participant_name for s in dorm_submissions))

    # 计算匹配度分数（简化计算）
    match_scores = []
    for submission in dorm_submissions:
        # 查找对应的室友答题记录
        roommate_submissions = [
            sub
            for sub in quiz_submissions
            if (
                sub.dormitory_id == dormitory_id
                and sub.target_roommate == submission.participant_name
                and sub.participant_name == submission.target_roommate
            )
        ]

        if roommate_submissions:
            roommate_submission = roommate_submissions[0]
            matched_count = 0
            for question_id, answer_index in submission.answers.items():
                if question_id in roommate_submission.answers:
                    if answer_index == roommate_submission.answers[question_id]:
                        matched_count += 1

            match_percentage = (
                matched_count / len(submission.answers) if submission.answers else 0
            )
            match_scores.append(int(match_percentage * 100))

    average_match_score = sum(match_scores) / len(match_scores) if match_scores else 0
    best_match_score = max(match_scores) if match_scores else 0

    # 计算排名
    match_rankings = {}
    if match_scores:
        sorted_scores = sorted(match_scores, reverse=True)
        for i, score in enumerate(sorted_scores):
            match_rankings[f"第{i + 1}名"] = score

    last_submission = max(dorm_submissions, key=lambda x: x.submitted_at)

    return DormitoryMatchStats(
        dormitory_id=dormitory_id,
        total_participants=total_participants,
        average_match_score=average_match_score,
        best_match_score=best_match_score,
        total_submissions=len(dorm_submissions),
        last_submission_time=last_submission.submitted_at,
        match_rankings=match_rankings,
    )


@router.get("/leaderboard", response_model=List[MatchResult])
async def get_leaderboard():
    """获取匹配度排行榜"""
    if not quiz_submissions:
        return []

    # 计算每个参与者的匹配度
    participant_matches = {}
    for submission in quiz_submissions:
        # 查找对应的室友答题记录
        roommate_submissions = [
            sub
            for sub in quiz_submissions
            if (
                sub.dormitory_id == submission.dormitory_id
                and sub.target_roommate == submission.participant_name
                and sub.participant_name == submission.target_roommate
            )
        ]

        if roommate_submissions:
            roommate_submission = roommate_submissions[0]
            matched_count = 0
            for question_id, answer_index in submission.answers.items():
                if question_id in roommate_submission.answers:
                    if answer_index == roommate_submission.answers[question_id]:
                        matched_count += 1

            match_percentage = (
                matched_count / len(submission.answers) if submission.answers else 0
            )
            match_score = int(match_percentage * 100)

            # 确定匹配等级
            if match_score >= 90:
                match_level = "心灵相通"
                analysis = "你们简直是天生一对的室友！"
            elif match_score >= 70:
                match_level = "默契十足"
                analysis = "你们的默契度很高，相处很愉快！"
            elif match_score >= 50:
                match_level = "互相了解"
                analysis = "你们对彼此有一定了解，继续加油！"
            else:
                match_level = "还需磨合"
                analysis = "还需要更多时间互相了解哦～"

            key = (
                submission.participant_name,
                submission.dormitory_id,
                submission.target_roommate,
            )
            if (
                key not in participant_matches
                or match_score > participant_matches[key]["score"]
            ):
                participant_matches[key] = {
                    "score": match_score,
                    "matched_count": matched_count,
                    "total_questions": len(submission.answers),
                    "match_level": match_level,
                    "analysis": analysis,
                }

    # 转换为排行榜结果
    leaderboard = []
    for (
        participant_name,
        dormitory_id,
        target_roommate,
    ), match_data in participant_matches.items():
        leaderboard.append(
            MatchResult(
                participant_name=participant_name,
                dormitory_id=dormitory_id,
                target_roommate=target_roommate,
                matched_count=match_data["matched_count"],
                total_questions=match_data["total_questions"],
                match_percentage=match_data["score"],
                match_level=match_data["match_level"],
                analysis=match_data["analysis"],
                rank=0,  # 将在排序后设置
            )
        )

    # 按匹配度排序并设置排名
    leaderboard.sort(key=lambda x: x.match_percentage, reverse=True)
    for i, result in enumerate(leaderboard):
        result.rank = i + 1

    return leaderboard
