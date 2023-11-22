from json import load, dump

from gryphon.github import GithubPackage
from gryphon.package import Package
from logging import get_logger


class Gryphon:
    internal_packages = [
        GithubPackage("mvanderlugt", "micropython-gryphon", "main"),
        GithubPackage("mvanderlugt", "micropython-wifi", "main"),
        GithubPackage("mvanderlugt", "micropython-http-client", "main"),
        GithubPackage("mvanderlugt", "micropython-logging", "main")
    ]

    def __init__(self):
        self.log = get_logger(__name__)
        self.filename = "gryphon.json"
        self.package_registry: dict = dict()

    async def load_registry(self) -> None:
        config = self.load_config()
        if "packages" in config:
            self.package_registry = config["packages"]
        else:
            self.package_registry = dict()

    async def save_registry(self) -> None:
        config = self.load_config()
        config["packages"] = self.package_registry
        self.save_config(config)

    async def self_update(self):
        for package in Gryphon.internal_packages:
            await self.update_package(package)

    async def update_build(self):
        from build import packages

        for package in packages:
            await self.update_package(package)

    async def update_package(self, package: Package) -> None:
        latest_version = await package.get_latest_version()
        if package.get_id() not in self.package_registry or \
                self.package_registry[package.get_id()]["version"] != latest_version:
            self.log.info(f"Installing {package}, version = {latest_version}")
            await package.install(latest_version)
            await self.update_registry_package_version(package, latest_version)
            await self.save_registry()
        else:
            self.log.info(f"{package} already latest version")

    async def update_registry_package_version(self, package, latest_version):
        if package.get_id() not in self.package_registry:
            self.package_registry[package.get_id()] = dict()
        self.package_registry[package.get_id()] = dict(version=latest_version)

    def load_config(self) -> dict:
        try:
            with open(self.filename) as stream:
                config = load(stream)
        except OSError as error:
            if error.errno == 2:
                with open(self.filename, "w") as file:
                    file.write("{}")
                config = dict()
            else:
                raise error
        return config

    def save_config(self, config: dict) -> None:
        with open(self.filename, 'w') as stream:
            dump(config, stream)
