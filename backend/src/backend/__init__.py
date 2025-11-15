from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .wordcloud import router as wordcloud_router


def create_app() -> FastAPI:
    app = FastAPI(title="寝室文化节API", version="1.0.0")

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
    app.include_router(wordcloud_router)

    return app


app = create_app()
