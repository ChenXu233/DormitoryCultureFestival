from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
from backend.config import CONFIG

router = APIRouter(prefix="/ai", tags=["ai"])

class GenerateImageRequest(BaseModel):
    prompt: str
    image_url: str
    model: str = "doubao-seedream-4-0-250828"
    size: str = "2K"
    watermark: bool = False

@router.post("/generate-image")
async def generate_image(request: GenerateImageRequest):
    api_key = CONFIG.ARK_API_KEY
    if not api_key:
        # Fallback to check if it's passed in header or we can't proceed
        # For now, assume it must be in config. 
        # If user hasn't set it in backend .env, this will fail.
        # But wait, the frontend had it. The user might not have set it in backend .env yet.
        # I should probably allow passing it from frontend if not in backend config?
        # But for security, backend config is better.
        # Let's assume user will set it in .env or I can try to read it from os.environ if pydantic didn't pick it up (it should).
        raise HTTPException(status_code=500, detail="ARK_API_KEY not configured in backend")

    # 1. Call Volcengine API
    url = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": request.model,
        "prompt": request.prompt,
        "image": request.image_url,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": request.size,
        "stream": False,
        "watermark": request.watermark
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers, timeout=120.0) # Increased timeout
            if response.status_code != 200:
                 # Try to parse error
                try:
                    err_data = response.json()
                    detail = err_data.get("error", {}).get("message", str(response.content))
                except:
                    detail = str(response.content)
                raise HTTPException(status_code=response.status_code, detail=f"AI API Error: {detail}")
            
            data = response.json()
            if not data.get("data") or not data["data"][0].get("url"):
                 raise HTTPException(status_code=500, detail="Invalid response from AI API")
            
            image_url = data["data"][0]["url"]

        except httpx.RequestError as e:
             raise HTTPException(status_code=500, detail=f"Request to AI API failed: {e}")

    # 2. Stream the image back
    async def iter_file():
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("GET", image_url, follow_redirects=True) as response:
                    if response.status_code != 200:
                        raise HTTPException(status_code=response.status_code, detail="Failed to fetch generated image")
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except httpx.RequestError as exc:
                raise HTTPException(status_code=500, detail=f"Error fetching image: {exc}")

    return StreamingResponse(iter_file(), media_type="image/png")
