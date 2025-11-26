from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router.wordcloud import router as wordcloud_router
from .router.quiz import router as quiz_router
from .router.certificate import router as certificate_router
from .database import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifepan(app: FastAPI):
    # Initialize database or other startup tasks
    await init_db()
    try:
        # yield control back to FastAPI so the app runs
        yield
    finally:
        # Optional cleanup/shutdown logic can go here, e.g. closing DB connections
        pass

origins = [
    "http://localhost:3000",   # 本地开发前端
    "http://101.126.35.203:3000",  # 如果你部署了前端在这个服务器
    # "*" 也可以用来允许所有来源，但不推荐生产环境使用
]

def create_app() -> FastAPI:
    app = FastAPI(title="寝室文化节API", version="1.0.0", lifespan=lifepan)

    # 配置CORS中间件，允许前端访问
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # 生产环境应该配置具体的域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 根路径
    @app.get("/")
    def read_root():
        return {"message": "寝室文化节API服务正在运行"}

    # 健康检查
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    # 包含词云路由
    app.include_router(wordcloud_router, prefix="/api")

    # 包含答题模块路由
    app.include_router(quiz_router, prefix="/api")

    # 包含证书模块路由
    app.include_router(certificate_router, prefix="/api")
    return app


app = create_app()
