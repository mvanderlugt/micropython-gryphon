from gryphon.package import Package


class Gryphon:
    def __init__(self):
        from build import packages
        self.packages: list[Package] = packages

    def check_for_updates(self):
        for package in self.packages:
            latest_version = package.get_latest_version()
            package.install(latest_version)
