import os
from datetime import datetime
from typing import List
import pandas as pd

from startrack.config import GITHUB_TOKEN_ENV
from startrack.core import (
    list_organization_repositories,
    RepositoryType,
    RepositoryData,
    to_dataframe
)

GITHUB_TOKEN = os.environ.get(GITHUB_TOKEN_ENV, None)
ORGANIZATION_NAMES = ["roboflow", "autodistill"]


def save_to_csv(df: pd.DataFrame, directory: str, filename: str) -> None:
    """
    Save a DataFrame to a CSV file in the specified directory.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        directory (str): The directory where the CSV file will be saved.
        filename (str): The name of the CSV file.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)
    df.to_csv(file_path)


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


all_repositories_json = []
for organization_name in ORGANIZATION_NAMES:
    repositories_json = get_all_organization_repositories(
        github_token=GITHUB_TOKEN,
        organization_name=organization_name,
        repository_type=RepositoryType.PUBLIC)
    all_repositories_json.extend(repositories_json)

repositories = [
    RepositoryData.from_json(repository_json)
    for repository_json
    in all_repositories_json]
df = to_dataframe(repositories)
df = df.set_index('full_name').T

current_date = datetime.now().strftime("%Y-%m-%d")
df.index = [current_date]

save_to_csv(
    df=df,
    directory='data',
    filename='data.csv')
