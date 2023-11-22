
class Package:
    async def get_latest_version(self) -> str:
        raise NotImplementedError()

    async def install(self, version: str) -> None:
        raise NotImplementedError()
