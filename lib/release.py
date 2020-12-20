from git import Repo
from semver import VersionInfo
from pathlib import Path
import argparse

OUT_DIR = Path("output")
OVA_DIR = OUT_DIR.joinpath("ova")
BOX_DIR = OUT_DIR.joinpath("box")
GIT_LATEST_TAG = Repo().tags[-1].name
LATEST_VERSION = VersionInfo.parse(GIT_LATEST_TAG[1:])
RELEASE_VERSION = LATEST_VERSION.bump_patch()
GIT_RELEASE_TAG = f"v{RELEASE_VERSION}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--owner", required=True)
    args = parser.parse_args()
    ovas = list(OVA_DIR.rglob("*.ova"))
    boxes = list(BOX_DIR.rglob("*.box"))
    files = [*ovas, *boxes]
    files = sorted(files, key=lambda f: f.absolute())
    files = {f.name: f for f in files if f.name not in files}
    if args.debug:
        for file in files:
            print(files[file].name)
    files = [str(f) for f in files.values()]
    params = [
        "gh",
        "release",
    ]
    if bool(args.owner) and bool(args.repo):
        params += ["--repo", f"{args.owner}/{args.repo}"]
    params += [
        "create",
        "--title",
        GIT_RELEASE_TAG,
        GIT_RELEASE_TAG,
        *files,
    ]
    print(" ".join(params))


if __name__ == "__main__":
    main()
