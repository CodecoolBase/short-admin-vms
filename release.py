from git import Repo
from semver import VersionInfo
from pathlib import Path
from sys import argv

OUT_DIR = Path("output")
GIT_LATEST_TAG = Repo().tags[-1].name
LATEST_VERSION = VersionInfo.parse(GIT_LATEST_TAG[1:])
RELEASE_VERSION = LATEST_VERSION.bump_patch()
GIT_RELEASE_TAG = f"v{RELEASE_VERSION}"


def main():
    template = argv[1] if len(argv) > 1 else "ubuntu-18.04"
    ovas = list(OUT_DIR.rglob(f"{template}-*.ova"))
    ovas = sorted(ovas, key=lambda ova: ova.absolute())
    ovas = {ova.name: ova for ova in ovas if ova.name not in ovas}
    ovas = [str(ova) for ova in ovas.values()]
    print(
        " ".join(
            [
                "gh",
                "release",
                "create",
                "--title",
                GIT_RELEASE_TAG,
                GIT_RELEASE_TAG,
                *ovas,
            ]
        )
    )


if __name__ == "__main__":
    main()
