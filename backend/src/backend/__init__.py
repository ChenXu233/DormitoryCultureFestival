from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.router.wordcloud import router as wordcloud_router
from backend.router.quiz import router as quiz_router
from backend.router.certificate import router as certificate_router
from backend.router.upload import router as upload_router
from backend.router.utils import router as utils_router
from backend.router.ai import router as ai_router
from backend.database import init_db
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles


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


def create_app() -> FastAPI:
    app = FastAPI(title="寝室文化节API", version="1.0.0", lifespan=lifepan)

    # 配置CORS中间件，允许前端访问
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 生产环境应该配置具体的域名
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
    
    app.include_router(upload_router, prefix="/api")
    app.include_router(utils_router, prefix="/api")
    app.include_router(ai_router, prefix="/api")
    return app


app = create_app()


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)