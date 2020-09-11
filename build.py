from git import Repo
from jinja2 import Environment, FileSystemLoader
from os import environ
from pathlib import Path
from sys import argv
from tempfile import NamedTemporaryFile, TemporaryDirectory

import subprocess
import yaml

DEBUG = "DEBUG" in environ
OUT_DIR = Path("output")
GIT_COMMIT_HASH = Repo().head.object.hexsha


def get_context(template, variant, variant_path):
    with variant_path.open() as f:
        context = yaml.safe_load(f)
    context["template"] = template
    context["variant"] = variant
    context["scripts_dir"] = f"templates/{template}/scripts"
    context["git_commit_hash"] = GIT_COMMIT_HASH
    return context


def get_base_context(template, variant, variant_path, preseed_template_path):
    context = get_context(template, variant, variant_path)
    context["http_directory"] = preseed_template_path.parent.as_posix()
    context["preseed_file_name"] = preseed_template_path.name
    return context


def get_next_context(template, variant, variant_path):
    context = get_context(template, variant, variant_path)
    base_ovas = list(OUT_DIR.rglob(f"{template}-base-*.ova"))
    base_ovas.sort(reverse=True)
    if len(base_ovas) == 0:
        raise ValueError("No base OVA found to build upon")
    base_ova = base_ovas[0]
    context["base_path"] = base_ova.as_posix()
    context["base_name"] = base_ova.name
    return context


def get_packer_j2_template(template, variant):
    if variant != "base":
        variant = "next"
    return Environment(
        loader=FileSystemLoader(f"templates/{template}"),
        variable_start_string="{$",
        variable_end_string="$}",
    ).get_template(f"{variant}.json.j2")


def get_preseed_j2_template(template):
    return Environment(
        loader=FileSystemLoader(f"templates/{template}/preseed"),
        variable_start_string="{$",
        variable_end_string="$}",
    ).get_template("base.cfg.j2")


def render_packer_template(path, context):
    with path.open(mode="w+") as f:
        j2_template = get_packer_j2_template(context["template"], context["variant"])
        f.write(j2_template.render(context))
        f.close()


def render_preseed_template(path, context):
    with path.open(mode="w+") as f:
        j2_template = get_preseed_j2_template(context["template"])
        f.write(j2_template.render(context))
        f.close()


def packer_build(work_dir, template, variant, variant_path):
    if variant == "base":
        preseed_template_path = work_dir.joinpath(f"{template}-base.cfg")
        context = get_base_context(
            template, variant, variant_path, preseed_template_path
        )
        render_preseed_template(preseed_template_path, context)
        if DEBUG:
            print(preseed_template_path)
            print(preseed_template_path.read_text())

    else:
        context = get_next_context(template, variant, variant_path)

    packer_template_path = work_dir.joinpath(f"{template}-{variant}.json")
    render_packer_template(packer_template_path, context)
    if DEBUG:
        print(packer_template_path)
        print(packer_template_path.read_text())

    proc = subprocess.run(
        ["packer", "build", "-var", f"name={template}-{variant}", packer_template_path],
        check=True,
    )


def build(template, variant):
    templates_dir = Path("templates")
    templates = [f.name for f in templates_dir.iterdir() if f.is_dir()]
    if not template in templates:
        raise ValueError(
            f"Unknown template: {template}, available templates: {', '.join(templates)}"
        )

    variants_dir = templates_dir.joinpath(template).joinpath("variants")
    variants = {f.name.split(f.suffix)[0]: f for f in list(variants_dir.glob("*.yml"))}
    if not variant in variants:
        raise ValueError(
            f"Unknown variant: {variant}, available variants: {', '.join(variants.keys())}"
        )

    with TemporaryDirectory() as work_dir:
        packer_build(Path(work_dir), template, variant, variants[variant])


def main():
    template = argv[1] if len(argv) > 1 else None
    variant = argv[2] if len(argv) > 2 else "all"
    build(template, variant)


if __name__ == "__main__":
    main()
