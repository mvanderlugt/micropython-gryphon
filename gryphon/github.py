
class GithubPackage:
    def __init__(self, owner: str, package: str, version: str = "main"):
        self.owner = owner
        self.package = package
        self.version = version

