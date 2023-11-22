
class Package:
    def get_latest_version(self) -> str:
        raise NotImplementedError()

    def install(self, version: str) -> None:
        raise NotImplementedError()
