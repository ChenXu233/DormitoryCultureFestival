from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import httpx

router = APIRouter(
    prefix="/utils",
    tags=["utils"]
)

@router.get("/proxy-image")
async def proxy_image(url: str = Query(..., description="The URL of the image to proxy")):
    """
    Proxy an image from a remote URL to avoid CORS issues.
    """
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    async def iter_file():
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("GET", url, follow_redirects=True) as response:
                    if response.status_code != 200:
                        raise HTTPException(status_code=response.status_code, detail="Failed to fetch image")
                    
                    async for chunk in response.aiter_bytes():
                        yield chunk
            except httpx.RequestError as exc:
                raise HTTPException(status_code=500, detail=f"Error fetching image: {exc}")

    # We need to fetch the headers first to get the content type
    async with httpx.AsyncClient() as client:
        try:
            response = await client.head(url, follow_redirects=True)
            content_type = response.headers.get("content-type", "image/jpeg") # Default to jpeg if not found
        except:
            content_type = "image/jpeg"

    return StreamingResponse(iter_file(), media_type=content_type)
