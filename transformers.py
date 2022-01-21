from typing import Callable, Any


def apply_transformers(item: Any, *transformers: Callable) -> Any:
    for transformer in transformers:
        item = transformer(item)

    return item


def to_str(item: Any) -> str:
    return str(item)


def lower(item: str) -> str:
    return item.lower()


def rstrip(item: str) -> str:
    return item.rstrip()


def lstrip(item: str) -> str:
    return item.lstrip()
