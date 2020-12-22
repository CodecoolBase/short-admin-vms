from pathlib import Path
from re import match
from semver import VersionInfo
import argparse

OUT_DIR = Path("output")
OVA_DIR = OUT_DIR.joinpath("ova")
BOX_DIR = OUT_DIR.joinpath("box")


def main():
    def tag_type(x):
        if not match(r"^v\d+\.\d+.\d+$", x):
            raise argparse.ArgumentTypeError(
                f"invalid tag: '{x}', must be in vMAJOR.MINOR.PATCH version format (with a leading 'v')"
            )
        return x

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--tag", required=True, type=tag_type)
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
        args.tag,
        args.tag,
        *files,
    ]
    print(" ".join(params))


if __name__ == "__main__":
    main()
