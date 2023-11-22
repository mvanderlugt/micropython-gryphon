
class Package:
    def get_id(self) -> str:
        raise NotImplementedError

    async def get_latest_version(self) -> str:
        raise NotImplementedError()

    async def install(self, version: str) -> None:
        raise NotImplementedError()
