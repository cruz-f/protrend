from typing import Callable, List, Type

from django_neomodel import DjangoNode
from rest_framework import status

import domain.model_api as mapi
from domain.database.utils import protrend_id_decoder, protrend_id_encoder
from exceptions import ProtrendException
from transformers import apply_transformers, to_str, lower, rstrip, lstrip


# ------------------------------------------------
# VALIDATION OF THE DATABASE UNIQUE CONSTRAINS
# ------------------------------------------------
def _validate_factor(value: str, transformers: List[Callable]):
    return apply_transformers(value, *transformers)


def _validate_duplicates(value: str, transformers: List[Callable], node_cls: Type[DjangoNode], key: str):
    value = apply_transformers(value, *transformers)
    obj = mapi.get_object(node_cls, **{key: value})
    if obj is not None:
        raise ProtrendException(detail=f'Duplicated issue. There is a similar entry in the database with this {value} '
                                       f'value. Please check the following protrend_id: {obj.protrend_id}.',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)


def _get_last_idx(node_cls: Type[DjangoNode]) -> int:
    last_obj = mapi.get_last_object(node_cls, 'protrend_id')

    if last_obj:
        return protrend_id_decoder(last_obj.protrend_id)
    else:
        return 0


# ------------------------------------------------
# VALIDATION OF UNIQUENESS BY LOWER AND STRIP
# ------------------------------------------------
def _validate_kwargs_str(kwargs: dict, factor: str, node_cls: Type[DjangoNode], header: str, entity: str):
    _validate_duplicates(value=kwargs[factor],
                         transformers=[to_str, lower, rstrip, lstrip],
                         node_cls=node_cls,
                         key=f'{factor}_factor')

    idx = _get_last_idx(node_cls) + 1
    new_id = protrend_id_encoder(header=header, entity=entity, integer=idx)
    kwargs['protrend_id'] = new_id

    new_factor = _validate_factor(value=kwargs[factor], transformers=[to_str, lower, rstrip, lstrip])
    kwargs[f'{factor}_factor'] = new_factor
    return kwargs


def _validate_args_str(args: tuple, factor: str, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    for arg in args:
        _validate_duplicates(value=arg[factor],
                             transformers=[to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key=f'{factor}_factor')

    idx = _get_last_idx(node_cls) + 1
    for i, arg in enumerate(args):
        i = idx + i
        new_id = protrend_id_encoder(header=header, entity=entity, integer=i)
        arg['protrend_id'] = new_id

        new_factor = _validate_factor(value=arg[factor], transformers=[to_str, lower, rstrip, lstrip])
        arg[f'{factor}_factor'] = new_factor

    return args


# ------------------------------------------------
# VALIDATION OF THE NAME ATTRIBUTE
# ------------------------------------------------
def _validate_kwargs_by_name(kwargs: dict, node_cls: Type[DjangoNode], header: str, entity: str):
    kwargs = kwargs.copy()
    return _validate_kwargs_str(kwargs=kwargs, factor='name', node_cls=node_cls, header=header, entity=entity)


def _validate_args_by_name(args: tuple, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    return _validate_args_str(args=args, factor='name', node_cls=node_cls, header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE LOCUS TAG ATTRIBUTE
# ------------------------------------------------
def _validate_kwargs_by_locus_tag(kwargs: dict, node_cls: Type[DjangoNode], header: str, entity: str):
    kwargs = kwargs.copy()
    return _validate_kwargs_str(kwargs=kwargs, factor='locus_tag', node_cls=node_cls, header=header, entity=entity)


def _validate_args_by_locus_tag(args: tuple, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    return _validate_args_str(args=args, factor='locus_tag', node_cls=node_cls, header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE UNIPROT ACCESSION ATTRIBUTE
# ------------------------------------------------
def _validate_kwargs_by_uniprot_accession(kwargs: dict, node_cls: Type[DjangoNode]):
    kwargs = kwargs.copy()
    _validate_duplicates(value=kwargs['uniprot_accession'],
                         transformers=[to_str, lower, rstrip, lstrip],
                         node_cls=node_cls,
                         key='uniprot_accession_factor')

    new_factor = _validate_factor(value=kwargs['uniprot_accession'], transformers=[to_str, lower, rstrip, lstrip])
    kwargs['uniprot_accession_factor'] = new_factor
    return kwargs


def _validate_args_by_uniprot_accession(args: tuple, node_cls: Type[DjangoNode]):
    args = tuple(args)
    for arg in args:
        _validate_duplicates(value=arg['uniprot_accession'],
                             transformers=[to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key='uniprot_accession_factor')

    for arg in args:
        new_factor = _validate_factor(value=arg['uniprot_accession'], transformers=[to_str, lower, rstrip, lstrip])
        arg['uniprot_accession_factor'] = new_factor

    return args
