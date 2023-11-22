from mip import install

from gryphon.package import Package
from http_client import HttpClient


class GithubPackage(Package):
    def __init__(self, owner: str, repository: str, branch: str = "main"):
        self.owner = owner
        self.repository = repository
        self.branch = branch

    def get_id(self) -> str:
        return f"{self.owner}/{self.repository}"

    def __str__(self) -> str:
        return f"GithubPackage(owner='{self.owner}', repository='{self.repository}', branch='{self.branch}')"

    async def get_latest_version(self) -> str:
        http_client = HttpClient("api.github.com", 443, ssl=True)
        path = f"/repos/{self.owner}/{self.repository}/git/refs/heads/{self.branch}"
        headers = {
            "User-Agent": "gryphon/1.0.0",
            "Accept": "application/json"
        }
        response = await http_client.get(path, headers=headers)
        if response.status.code == 200:
            return response.body["object"]["sha"]

    async def install(self, git_sha: str):
        install(f"github:{self.owner}/{self.repository}", version=git_sha)
