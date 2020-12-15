import argparse
from .yaml_parser import yaml


def get_args(config):
    # First pass, unknown variants are ignored
    parser = _create_parser(config, True)
    known_args, remaining_args = parser.parse_known_args()
    _normalize_args(known_args)
    if known_args.debug:
        print(known_args, remaining_args)
    # For the second pass a stricter parser is used
    # and additional arguments are added dynamically
    parser = _create_parser(config, False, known_args.variants)
    args = parser.parse_args()
    _normalize_args(args)
    if args.debug:
        print(args)
    return args


def _create_parser(config, first_run, known_variants=[]):
    # TODO: available variants should be read from the config dynamically
    all_variants = ["root", "base", "nossh", "mininet", "desktop", "db", "www"]
    seen_variants = []

    def existing_variant_type(x):
        return x if x in all_variants else None

    def seen_variant_type(x):
        if x in seen_variants:
            raise argparse.ArgumentTypeError(f"invalid choice: '{x}' already choosen")
        seen_variants.append(x)
        if not x in all_variants:
            choices = ", ".join(map(lambda x: "'" + x + "'", all_variants))
            raise argparse.ArgumentTypeError(
                f"invalid choice: '{x}' (choose from {choices})"
            )
        return x

    def yaml_string(x):
        try:
            return yaml.load(x)
        except:
            raise argparse.ArgumentTypeError(f"invalid YAML string: {x}")

    def yaml_file(x):
        try:
            with open(x) as f:
                yaml.load(f)
            return x
        except:
            raise argparse.ArgumentTypeError(f"invalid YAML file: {x}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--unregister-root", action="store_true")
    parser.add_argument("--vagrant", action="store_true")
    distro_subparsers = parser.add_subparsers(title="distros", dest="distro", required=True)
    for distro in config["distros"]:
        if distro == 'defaults':
            continue
        distro_parser = distro_subparsers.add_parser(distro)

        release_subparsers = distro_parser.add_subparsers(title="releases", dest="release", required=True)

        releases = list(config["distros"][distro])
        for release in releases:
            if release == 'defaults':
                continue
            release_parser = release_subparsers.add_parser(release)

            release_parser.add_argument(
                "variants",
                metavar="variant",
                type=existing_variant_type if first_run else seen_variant_type,
                nargs="*",
                default=all_variants,
            )
            for variant in known_variants:
                release_parser.add_argument(
                    f"--extra-{variant}-config", type=yaml_string, action="append"
                )
                release_parser.add_argument(
                    f"--extras-{variant}-config-file", type=yaml_file
                )
    return parser


def _normalize_args(args):
    # During the first pass invalid variants are ignored and represented with `None`
    # in the available list of variants, filtering them out for good measure
    args.variants = [x for x in args.variants if not x == None]

    # The `root` variant must always be the first thing to be built when present
    if "root" in args.variants:
        args.variants.pop(args.variants.index("root"))
        args.variants.insert(0, "root")
