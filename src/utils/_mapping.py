from enum import Enum
from typing import Any, Dict, Sequence, Tuple
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


def string_to_hex(hex_str: str) -> int:
    """
    `#EE5670` => `0xFFEE5670`

    Args:
        hex (str): hex string starting with #.

    Returns:
        int: hex value
    """
    return int(hex_str[1:], 16)


def indexed_(data: Sequence) -> str:
    """
    Transform data into structured string.

    Args:
        data (Sequence)

    Returns:
        str: transformed data

    Examples:
        >>> indexed_([item1, item2, ..., itemN])
        1. item1
        2. item2
        ...
        n. itemN
    """
    return ('\n'.join([f'{index}. {item}' 
            for index, item in enumerate(data, start=1)]))


def counted_(data: Sequence) -> str:
    """
    Transform data into stuctured string.

    Args:
        data (Sequence)

    Returns:
        str: transformed data

    Examples:
        >>> counted_([item1, item1, item2, ..., itemN])
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


class BorderStyle(Enum):
    ROUNDED = "rounded"
    PLAIN = "plain"
    DOUBLE = "double"
    MINIMAL = "minimal"

class AlignStyle(Enum):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"


def tabled_(
    data: Dict[Any, Any],
    headers: Tuple[str, str] = ("Key", "Value"),
    *,
    border_style: BorderStyle = BorderStyle.ROUNDED,
    align: AlignStyle = AlignStyle.LEFT,
    padding: int = 1,
    sort_keys: bool = False,
) -> str:
    """
    Convert a dictionary into a pretty formatted table.

    Args:
        data: Input dictionary to display.
        headers: Column headers (Key, Value).
        border_style: Table border style `BorderStyle.ROUNDED/PLAIN/DOUBLE/MINIMAL`.
        align: Text alignment `AlignStyle.LEFT/RIGHT/CENTER`.
        padding: Inner padding around text.
        sort_keys: Sort dictionary keys alphabetically.

    Returns:
        Formatted table as a string.

    Example:
        >>> data = {"Apple": 3, "Banana": 2, "Orange": 1}
        >>> print(tabled_(data))
        ╭──────────┬───────╮
        │   Key    │ Value │
        ├──────────┼───────┤
        │  Apple   │   3   │
        │  Banana  │   2   │
        │  Orange  │   1   │
        ╰──────────┴───────╯
    """
    if not data:
        return "No data to display."
    
    border_str = border_style.value
    align_str = align.value

    borders = {
        "rounded": ("╭", "┬", "╮", "├", "┼", "┤", "╰", "┴", "╯", "─", "│"),
        "plain": ("┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘", "─", "│"),
        "double": ("╔", "╦", "╗", "╠", "╬", "╣", "╚", "╩", "╝", "═", "║"),
        "minimal": (" ", " ", " ", "─", "─", " ", " ", " ", " ", "─", "│"),
    }
    border = borders.get(border_str, borders["rounded"])

    key_width = max(len(str(k)) for k in data.keys())
    val_width = max(len(str(v)) for v in data.values())
    key_width = max(key_width, len(headers[0])) + 2 * padding
    val_width = max(val_width, len(headers[1])) + 2 * padding

    top = f"{border[0]}{border[9] * key_width}{border[1]}{border[9] * val_width}{border[2]}"
    header = (
        f"{border[10]}{str(headers[0]).center(key_width) if align == AlignStyle.CENTER else str(headers[0]).ljust(key_width)}"
        f"{border[10]}{str(headers[1]).center(val_width) if align == AlignStyle.CENTER else str(headers[1]).ljust(val_width)}"
        f"{border[10]}"
    )
    separator = f"{border[3]}{border[9] * key_width}{border[4]}{border[9] * val_width}{border[5]}"
    bottom = f"{border[6]}{border[9] * key_width}{border[7]}{border[9] * val_width}{border[8]}"

    align_func = {
        "left": str.ljust,
        "right": str.rjust,
        "center": str.center,
    }.get(align_str, str.ljust)

    rows = [top, header, separator]
    keys = sorted(data.keys()) if sort_keys else data.keys()
    for key in keys:
        key_str = align_func(str(key), key_width - 2 * padding)
        val_str = align_func(str(data[key]), val_width - 2 * padding)
        row = f"{border[10]}{' ' * padding}{key_str}{' ' * padding}{border[10]}{' ' * padding}{val_str}{' ' * padding}{border[10]}"
        rows.append(row)
    rows.append(bottom)

    return "\n".join(rows)