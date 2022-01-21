# -----------------
# SANITY CHECKS
# -----------------
from typing import Callable, List, Type

from django_neomodel import DjangoNode

import domain.model_api as mapi
from domain.database.utils import protrend_id_decoder
from transformers import apply_transformers


def _sanitize_factor(value: str, transformers: List[Callable]):
    return apply_transformers(value, *transformers)


def _sanitize_duplicates(value: str, transformers: List[Callable], node_cls: Type[DjangoNode], key: str):
    value = apply_transformers(value, *transformers)
    return mapi.get_object(node_cls, **{key: value})


def _sanitize_protrend_idx(node_cls: Type[DjangoNode]):
    last_obj = mapi.get_last_object(node_cls, 'protrend_id')

    if last_obj:
        return protrend_id_decoder(last_obj.protrend_id) + 1
    else:
        return 1
