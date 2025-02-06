from typing import Sequence
from collections import Counter
import re


def camel_to_snake(name: str) -> str:
    """
    `stringInCamelStyle` => `string_in_camel_style`

    Args:
        name (string): string to modify

    Returns:
        str: modified string
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def json_camel_to_snake(json: dict) -> dict:
    """
    Transforms keys in json to a snake style strings.
    * For more details see `camel_to_snake()` func.

    Args:
        json (dict): json to modify

    Returns:
        dict: modified json
    """
    kwargs = {}
    for key, value in json.items():
        kwargs[camel_to_snake(key)] = value

    return kwargs


def snake_to_camel(name: str) -> str:
    """
    `string_in_snake_style` => `stringInSnakeStyle`

    Args:
        name (string): string to modify

    Returns:
        str: modified string
    """
    parts = name.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def json_snake_to_camel(json: dict) -> dict:
    """
    Transforms keys in json to a camel style strings.
    * For more details see `snake_to_camel()` func.

    Args:
        json (dict): json to modify

    Returns:
        dict: modified json
    """
    kwargs = {}
    for key, value in json.items():
        kwargs[snake_to_camel(key)] = value

    return kwargs


def retrieve_name(x, Vars=vars()) -> str | None:
    """
    Returns the name of variable.

    Args:
        x (variable): variable which name should be returned

    Returns:
        str | None: variable name
    """
    for k in Vars:
        if isinstance(x, type(Vars[k])):
            if x is Vars[k]:
                return k
    return None


def string_to_hex(hex: str) -> int:
    """
    `#EE5670` => `0xFFEE5670`

    Args:
        hex (str): hex string starting with #.

    Returns:
        int: hex value
    """
    return int(hex[1:], 16)


def indexed_(data: Sequence) -> str:
    """
    Transform data into structured string.

    Args:
        data (Sequence): `example` [item1, item2, ..., itemN]

    Returns:
        str: transformed data in format:
        ```
        1. item1
        2. item2
        ...
        n. itemN
        ```
    """
    return ('\n'.join([f'{index}. {item}' 
            for index, item in enumerate(data, start=1)]))


def counted_(data: Sequence) -> str:
    """
    Transform data into stuctured string.

    Args:
        data (Sequence): `example` [item1, item1, item2, ..., itemN]

    Returns:
        str: transformed data in format:
        ```
        item1: 2
        item2: 1
        ...
        itemN: m
    """
    counts = Counter(data)
    result = ""
    for key, value in counts.items():
        result += f'{key}: {value}\n'
    return result.strip()


from src.models import Asset
from src.models.asset_types import *

def handle_asset_data(data: dict) -> dict:
    """
    Support func for handling inventory items unboxing from json.

    Args:
        data (dict): json data from API with inventory items

    Returns:
        dict: json data with initializated Asset objects
    """
    for key in ["lootboxGif", "itemThumbnail"]:
        if key in data and data[key]:
            asset_data = data[key]
            asset_data["type"] = AssetTypes(asset_data["type"])
            for gif_key, gif_type in [
                ("gifType", GifTypes),
                ("interAction", InteractionActions),
                ("interType", InteractionTypes)
            ]:
                if gif_key in asset_data and asset_data[gif_key]:
                    asset_data[gif_key] = gif_type(asset_data[gif_key])
            data[key] = Asset(**json_camel_to_snake(asset_data))
    return data
