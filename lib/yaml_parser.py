from ruamel.yaml import YAML

yaml = YAML()
yaml.default_flow_style = False
yaml.representer.ignore_aliases = lambda *data: True
