from handlers.repo import Repository_short_url
from config import logger
from fastapi import HTTPException


class ServiceReductionUrl:

    def __init__(self, repo: Repository_short_url):
        self.repo = repo

    def create_short_url(self, url: str) -> str:
        short_url = self.repo.create_short_url(url)
        logger.info(f"Успешно создана короткая ссылка - {short_url}")
        return short_url

    def get_short_url(self, code: str) -> str:
        short_url = self.repo.get_short_url(code)
        if short_url is None:
            raise HTTPException(status_code=404, detail="Данной ссылки нету")
        return short_url
