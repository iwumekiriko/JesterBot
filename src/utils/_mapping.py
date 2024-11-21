import re


def camel_to_snake(name: str) -> str:
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def json_camel_to_snake(json: dict) -> dict:
    kwargs = {}
    for key, value in json.items():
        kwargs[camel_to_snake(key)] = value

    return kwargs