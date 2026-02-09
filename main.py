from fastapi import FastAPI, Request, Depends
from starlette.responses import RedirectResponse

from config import logger
from handlers.depend import get_service
from handlers.service import ServiceReductionUrl

app = FastAPI()


@app.get("/{code}")
async def get_url(
        code: str,
        service: ServiceReductionUrl = Depends(get_service)
):
    url = service.get_short_url(code)
    logger.info(f"Shortening URL: {url}")
    return RedirectResponse(url)


@app.post("/shorten")
async def post_url(
        url: str,
        service: ServiceReductionUrl = Depends(get_service)
):
    logger.info(f"Shortening URL: {url}")
    return service.create_short_url(url)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=9797, timeout_keep_alive=120)
