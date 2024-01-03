import os
from typing import List

from startrack.config import GITHUB_TOKEN_ENV
from startrack.core import list_organization_repositories, RepositoryType, \
    RepositoryData

GITHUB_TOKEN = os.environ.get(GITHUB_TOKEN_ENV, None)
ORGANIZATION_NAME = "roboflow"


def get_all_organization_repositories(
    github_token: str,
    organization_name: str,
    repository_type: RepositoryType
) -> List:
    all_repositories = []
    page = 1
    while True:
        repos = list_organization_repositories(
            github_token=github_token,
            organization_name=organization_name,
            repository_type=repository_type,
            page=page)
        if not repos:
            break
        all_repositories.extend(repos)
        page += 1

    return all_repositories


repositories_json = get_all_organization_repositories(
    github_token=GITHUB_TOKEN,
    organization_name=ORGANIZATION_NAME,
    repository_type=RepositoryType.PUBLIC)
repositories = [
    RepositoryData.from_json(repository_json)
    for repository_json
    in repositories_json]

print(repositories)
