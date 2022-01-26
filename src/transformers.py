from types import GeneratorType
from typing import Callable, Any, List, Union

import numpy as np
import pandas as pd


def apply_transformers(item: Any, *transformers: Callable) -> Any:
    for transformer in transformers:
        item = transformer(item)

    return item


def is_null(obj: Any) -> bool:
    # booleans
    if isinstance(obj, bool):
        return not obj

    # integers, floats, etc
    if isinstance(obj, (int, float)):
        return pd.isnull(obj)

    # numpy arrays
    if isinstance(obj, np.ndarray):
        return not obj.any()

    # pandas series and frames
    if isinstance(obj, (pd.DataFrame, pd.Series)):
        return obj.empty

    # python built-ins
    if isinstance(obj, (range, list, tuple, set, dict, frozenset, str)):
        return len(obj) == 0

    # python generator built-ins
    if isinstance(obj, GeneratorType):
        return False

    # pandas check for nan or null
    if pd.isnull(obj):
        return True

    return False


def to_str(item: Any) -> str:
    if is_null(item):
        return item

    try:
        return str(item)
    except (ValueError, TypeError):
        return item


def to_int(item: Any) -> int:
    if is_null(item):
        return item

    try:
        return int(item)
    except (ValueError, TypeError):
        return item


def lower(item: str) -> str:
    return item.lower()


def rstrip(item: str) -> str:
    return item.rstrip()


def lstrip(item: str) -> str:
    return item.lstrip()


def protrend_hash(items: List[str]) -> Union[None, str]:
    if is_null(items):
        return

    items = [to_str(item) for item in items]

    return '_'.join(items)
