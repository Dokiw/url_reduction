from handlers.repo import Repository_short_url
from handlers.service import ServiceReductionUrl


def get_service() -> ServiceReductionUrl:
    repo = Repository_short_url()
    return ServiceReductionUrl(repo)
