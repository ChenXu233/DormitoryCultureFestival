from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.router.quiz import router as quiz_router
from src.backend.router.wordcloud import router as wordcloud_router
from src.backend.database import init_db

# 创建FastAPI应用
app = FastAPI(title="宿舍文化节后端API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(quiz_router, prefix="/api")
app.include_router(wordcloud_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    await init_db()
    print("数据库初始化完成")


@app.get("/")
async def root():
    """根路径"""
    return {"message": "宿舍文化节后端API服务运行中"}


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
