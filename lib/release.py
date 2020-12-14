from git import Repo
from semver import VersionInfo
from pathlib import Path
from sys import argv
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
    parser.add_argument("--template", choices=["ubuntu"], default="ubuntu")
    parser.add_argument("--release", choices=["18.04", "20.04"], default="18.04")
    parser.add_argument("--repo")
    parser.add_argument("--owner")
    args = parser.parse_args()
    if bool(args.owner) ^ bool(args.repo):
        parser.error("--owner and --repo must be given together")
    ovas = list(OVA_DIR.rglob(f"{args.template}-{args.release}-*.ova"))
    boxes = list(BOX_DIR.rglob(f"{args.template}-{args.release}-*.box"))
    files = [*ovas, *boxes]
    files = sorted(files, key=lambda f: f.absolute())
    files = {f.name: f for f in files if f.name not in files}
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
