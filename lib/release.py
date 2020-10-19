from git import Repo
from semver import VersionInfo
from pathlib import Path
from sys import argv
import argparse

OUT_DIR = Path("output")
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
    ovas = list(OUT_DIR.rglob(f"{args.template}-{args.release}-*.ova"))
    ovas = sorted(ovas, key=lambda ova: ova.absolute())
    ovas = {ova.name: ova for ova in ovas if ova.name not in ovas}
    ovas = [str(ova) for ova in ovas.values()]
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
        *ovas,
    ]
    print(" ".join(params))


if __name__ == "__main__":
    main()
