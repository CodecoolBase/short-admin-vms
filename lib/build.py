from .argument_parser import get_args
from .j2 import j2_ctx, j2_path
from .merger_config import merger
from .webhook_server import run_webhook_server_thread
from .yaml_parser import yaml
from io import StringIO
from pathlib import Path
from sys import stdout
from tempfile import TemporaryDirectory
import inspect
import subprocess


def _get_paths(args, work_dir, variant):
    output_dir = Path("output")
    files_dir = Path("files").absolute()
    template_dir = Path(f"templates/{args.template}")
    scripts_dir = template_dir.joinpath("scripts")
    config_yml_file = template_dir.joinpath("config.yml")
    work_dir = Path(work_dir)
    build_dir = work_dir.joinpath(variant)
    build_dir.mkdir()
    if args.debug:
        print(f"output_dir: {output_dir}")
        print(f"files_dir: {files_dir}")
        print(f"template_dir: {template_dir}")
        print(f"scripts_dir: {scripts_dir}")
        print(f"config_yml_file: {config_yml_file}")
        print(f"work_dir: {work_dir}")
        print(f"build_dir: {build_dir}")
    return {
        "output_dir": output_dir,
        "files_dir": files_dir,
        "template_dir": template_dir,
        "scripts_dir": scripts_dir,
        "config_yml_file": config_yml_file,
        "work_dir": work_dir,
        "build_dir": build_dir,
    }


def _get_context(args, paths, variant, webhook_server_address):
    config = yaml.load(paths["config_yml_file"])
    context = {
        "variant": variant,
        "args": {k: getattr(args, k) for k in vars(args)},
        "paths": {k: v.as_posix() for k, v in paths.items()},
        "dynamic": {
            "webhook_server_address": webhook_server_address[0],
            "webhook_server_port": webhook_server_address[1],
        },
    }
    merger.merge(context, config["defaults"])
    merger.merge(context, config["releases"][args.release])
    merger.merge(context, config["variants"][variant])
    extras_config_file = getattr(args, f"extras_{variant}_config_file")
    if extras_config_file:
        with open(extras_config_file) as f:
            merger.merge(context, yaml.load(f))
    for member in inspect.getmembers(args):
        if member[0] == f"extra_{variant}_config" and member[1]:
            if args.debug:
                print(member)
            for extra in member[1]:
                merger.merge(context, extra)
    for key in context:
        if key in config["j2_template_fields"]:
            j2_ctx(context, key)
    if args.debug:
        yaml.dump(context, stdout)
    return context


def _get_template(args, paths, context):
    packer_j2_file = Path(paths["template_dir"].joinpath(context["packer_j2_name"]))
    template = j2_path(context, packer_j2_file)
    if args.debug:
        print(template)
    return template


def _build(args, paths, context, template):
    packer_template_json_file = paths["build_dir"].joinpath("packer.json")
    with packer_template_json_file.open("w+") as f:
        f.write(template)
    if "preseed" in context:
        preseed_cfg_file = paths["build_dir"].joinpath("preseed.cfg")
        with preseed_cfg_file.open("w+") as f:
            f.write(context["preseed"])
    if "cloud-init" in context:
        user_data_file = paths["build_dir"].joinpath("user-data")
        meta_data_file = paths["build_dir"].joinpath("meta-data")
        with user_data_file.open("w+") as f:
            user_data = context["cloud-init"]["user-data"]
            if user_data:
                with StringIO() as s:
                    yaml.dump(user_data, s)
                    f.write(s.getvalue().lstrip())
        with meta_data_file.open("w+") as f:
            meta_data = context["cloud-init"]["meta-data"]
            if meta_data:
                with StringIO() as s:
                    yaml.dump(meta_data, s)
                    f.write(s.getvalue().lstrip())
    if not args.dry_run:
        subprocess.run(
            [
                "packer",
                "build",
                "-var",
                f'name={args.template}-{args.release}-{context["variant"]}',
                packer_template_json_file,
            ],
            check=True,
        )


def _unregister_base(args):
    subprocess.run(
        [
            "VBoxManage",
            "unregistervm",
            f"packer-{args.template}-{args.release}-base",
            "--delete",
        ]
    )


def main():
    with TemporaryDirectory() as work_dir:
        args = get_args()
        webhook_server_address = run_webhook_server_thread(args)
        for variant in args.variants:
            paths = _get_paths(args, work_dir, variant)
            context = _get_context(args, paths, variant, webhook_server_address)
            template = _get_template(args, paths, context)
            _build(args, paths, context, template)
        if "base" in args.variants and not args.keep_base_registered:
            _unregister_base(args)


if __name__ == "__main__":
    main()
