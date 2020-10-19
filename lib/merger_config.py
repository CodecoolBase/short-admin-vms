from deepmerge import Merger


def _strategy_custom(config, path, base, nxt):
    if path[0] == "scripts_before":
        return base + nxt
    return nxt + base


merger = Merger([(list, _strategy_custom), (dict, "merge")], ["override"], [])
