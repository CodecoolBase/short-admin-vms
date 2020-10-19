from jinja2 import Environment
from passlib.hash import sha512_crypt


def j2_template(string):
    env = Environment(
        trim_blocks=False,
        lstrip_blocks=False,
        variable_start_string="{$",
        variable_end_string="$}",
    )
    env.filters["crypt"] = lambda x: sha512_crypt.hash(x, rounds=5000)
    return env.from_string(string if type(string) == str else str(string))


def j2_path(context, path):
    with path.open() as f:
        return j2_template(f.read()).render(context)


def j2_str(ctx, string):
    if type(string) == str:
        return j2_template(string).render(ctx)
    yaml_type = type(string)
    return yaml_type(j2_template(str(string)).render(ctx))


def j2_list(ctx, lst):
    for i in range(len(lst)):
        if isinstance(lst[i], dict):
            j2_dict(ctx, lst[i])
        elif isinstance(lst[i], list):
            j2_list(ctx, lst[i])
        elif isinstance(lst[i], str):
            lst[i] = j2_str(ctx, lst[i])
        elif isinstance(lst[i], (bool, int, float, type(None))):
            pass
        else:
            raise ValueError(f"Cannot handle {type(lst[i])}")


def j2_dict(ctx, dct):
    for k in dct:
        if isinstance(dct[k], dict):
            j2_dict(ctx, dct[k])
        elif isinstance(dct[k], list):
            j2_list(ctx, dct[k])
        elif isinstance(dct[k], str):
            dct[k] = j2_str(ctx, dct[k])
        elif isinstance(dct[k], (bool, int, float, type(None))):
            pass
        else:
            raise ValueError(f"Cannot handle {type(dct[k])}")


def j2_ctx(ctx, key):
    if isinstance(ctx[key], dict):
        j2_dict(ctx, ctx[key])
    elif isinstance(ctx[key], list):
        j2_list(ctx, ctx[key])
    elif isinstance(ctx[key], str):
        ctx[key] = j2_str(ctx, ctx[key])
    elif isinstance(ctx[key], (bool, int, float, type(None))):
        pass
    else:
        raise ValueError(f"Cannot handle {type(ctx[key])}")
