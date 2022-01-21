# -----------------
# VALIDATION TESTS
# -----------------
from typing import Callable, List, Type

from django_neomodel import DjangoNode
from rest_framework import status

import domain.model_api as mapi
from domain.database.utils import protrend_id_decoder, protrend_id_encoder
from exceptions import ProtrendException
from transformers import apply_transformers, to_str, lower, rstrip, lstrip


def _validate_factor(value: str, transformers: List[Callable]):
    return apply_transformers(value, *transformers)


def _validate_duplicates(value: str, transformers: List[Callable], node_cls: Type[DjangoNode], key: str):
    value = apply_transformers(value, *transformers)
    return mapi.get_object(node_cls, **{key: value})


def _sanitize_protrend_idx(node_cls: Type[DjangoNode]):
    last_obj = mapi.get_last_object(node_cls, 'protrend_id')

    if last_obj:
        return protrend_id_decoder(last_obj.protrend_id) + 1
    else:
        return 1


def _validate_kwargs_by_name(kwargs: dict, node_cls: Type[DjangoNode], header: str, entity: str):
    kwargs = kwargs.copy()
    obj = _validate_duplicates(value=kwargs['name'],
                               transformers=[to_str, lower, rstrip, lstrip],
                               node_cls=node_cls,
                               key='name_factor')

    if obj is not None:
        raise ProtrendException(detail=f'Object with name {obj.name} already exists in the database and '
                                       f'has the following protrend_id: {obj.protrend_id}',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    idx = _sanitize_protrend_idx(node_cls)
    new_id = protrend_id_encoder(header=header, entity=entity, integer=idx)
    kwargs['protrend_id'] = new_id

    new_factor = _validate_factor(value=kwargs['name'], transformers=[to_str, lower, rstrip, lstrip])
    kwargs['name_factor'] = new_factor
    return kwargs


def _validate_args_by_name(args: tuple, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    for arg in args:
        obj = _validate_duplicates(value=arg['name'],
                                   transformers=[to_str, lower, rstrip, lstrip],
                                   node_cls=node_cls,
                                   key='name_factor')

        if obj is not None:
            raise ProtrendException(detail=f'Object with name {obj.name} already exists in the database and '
                                           f'has the following protrend_id: {obj.protrend_id}',
                                    code='create error',
                                    status=status.HTTP_400_BAD_REQUEST)
    idx = _sanitize_protrend_idx(node_cls)

    for i, arg in enumerate(args):
        i = i + idx + 1
        new_id = protrend_id_encoder(header=header, entity=entity, integer=i)
        arg['protrend_id'] = new_id

        new_factor = _validate_factor(value=arg['name'], transformers=[to_str, lower, rstrip, lstrip])
        arg['name_factor'] = new_factor

    return args
