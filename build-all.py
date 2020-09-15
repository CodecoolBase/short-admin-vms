from build import build
from sys import argv
import subprocess

template = "ubuntu-18.04"
variants = ["base", "nossh", "mininet", "desktop", "db"] if len(argv) <= 1 else argv[1:]
for variant in variants:
    build(template, variant)
subprocess.run(["VBoxManage", "unregistervm", f"packer-{template}", "--delete"])
