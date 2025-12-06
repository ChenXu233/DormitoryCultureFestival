from fastapi import APIRouter, UploadFile, File, Form, Request, HTTPException
import os
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/upload", tags=["上传模块"])


@router.post("/image")
async def upload_image(request: Request, file: UploadFile = File(...), dormNumber: str = Form(None)):
    """接收图片文件，保存到 `backend/static/uploads`，返回可直接访问的 URL"""
    try:
        # 生成文件名
        _, ext = os.path.splitext(file.filename or "")
        if not ext:
            ext = ".png"
        filename = f"{(dormNumber or 'img')}_{uuid.uuid4().hex}{ext}"

        # 目标目录：项目根的 backend/static/uploads
        upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static', 'uploads'))
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, filename)
        # 保存文件
        content = await file.read()
        try:
            with open(file_path, "wb") as f:
                f.write(content)
                f.flush()
            logger.info('Saved uploaded file to %s', file_path)
        except Exception as write_err:
            logger.exception('Failed to write uploaded file to %s', file_path)
            raise HTTPException(status_code=500, detail=f'保存文件失败: {write_err}')

        # 确认文件存在以便调试
        exists = os.path.exists(file_path)
        logger.debug('File exists after write: %s -> %s', file_path, exists)

        # 使用请求的 base_url 构建可访问链接
        base_url = str(request.base_url)
        # 注意：main.py 中挂载了 /static
        url = f"{base_url}static/uploads/{filename}"

        # 返回包含可访问 url 和调试信息（开发时有用）
        return {"url": url, "path": file_path, "exists": exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
