from typing import Callable, List, Type

from django_neomodel import DjangoNode
from rest_framework import status

import domain.model_api as mapi
from domain.database.database_utils import protrend_id_decoder, protrend_id_encoder
from exceptions import ProtrendException
from transformers import apply_transformers, to_int, to_str, lower, rstrip, lstrip, protrend_hash


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
# VALIDATION OF UNIQUENESS BY HASH
# ------------------------------------------------
def _validate_kwargs_by_hash(kwargs: dict,
                             factor: str,
                             value: str,
                             node_cls: Type[DjangoNode],
                             header: str,
                             entity: str):
    _validate_duplicates(value=value,
                         transformers=[to_str, lower, rstrip, lstrip],
                         node_cls=node_cls,
                         key=f'{factor}_factor')

    idx = _get_last_idx(node_cls) + 1
    new_id = protrend_id_encoder(header=header, entity=entity, integer=idx)
    kwargs['protrend_id'] = new_id

    kwargs[factor] = value

    new_factor = _validate_factor(value=value, transformers=[to_str, lower, rstrip, lstrip])
    kwargs[f'{factor}_factor'] = new_factor
    return kwargs


def _validate_args_by_hash(args: tuple,
                           factor: str,
                           values: List[str],
                           node_cls: Type[DjangoNode],
                           header: str,
                           entity: str):
    for arg, value in zip(args, values):
        _validate_duplicates(value=value,
                             transformers=[to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key=f'{factor}_factor')

    idx = _get_last_idx(node_cls) + 1
    for i, (arg, value) in enumerate(zip(args, values)):
        i = idx + i
        new_id = protrend_id_encoder(header=header, entity=entity, integer=i)
        arg['protrend_id'] = new_id

        arg[factor] = value

        new_factor = _validate_factor(value=value, transformers=[to_str, lower, rstrip, lstrip])
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
    if 'uniprot_accession' not in kwargs:
        return kwargs

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
        if 'uniprot_accession' not in arg:
            continue

        _validate_duplicates(value=arg['uniprot_accession'],
                             transformers=[to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key='uniprot_accession_factor')

    for arg in args:
        if 'uniprot_accession' not in arg:
            continue

        new_factor = _validate_factor(value=arg['uniprot_accession'], transformers=[to_str, lower, rstrip, lstrip])
        arg['uniprot_accession_factor'] = new_factor

    return args


# ------------------------------------------------
# VALIDATION OF THE OPERON DB ID ATTRIBUTE
# ------------------------------------------------
def _validate_kwargs_by_operon_db_id(kwargs: dict, node_cls: Type[DjangoNode], header: str, entity: str):
    kwargs = kwargs.copy()
    return _validate_kwargs_str(kwargs=kwargs, factor='operon_db_id', node_cls=node_cls, header=header, entity=entity)


def _validate_args_by_operon_db_id(args: tuple, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    return _validate_args_str(args=args, factor='operon_db_id', node_cls=node_cls, header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE NCBI TAXONOMY ATTRIBUTE
# ------------------------------------------------
def _validate_kwargs_by_ncbi_taxonomy(kwargs: dict, node_cls: Type[DjangoNode]):
    kwargs = kwargs.copy()
    if 'ncbi_taxonomy' not in kwargs:
        return kwargs

    _validate_duplicates(value=kwargs['ncbi_taxonomy'],
                         transformers=[to_int, to_str, lower, rstrip, lstrip],
                         node_cls=node_cls,
                         key='ncbi_taxonomy_factor')

    new_factor = _validate_factor(value=kwargs['ncbi_taxonomy'], transformers=[to_int, to_str, lower, rstrip, lstrip])
    kwargs['ncbi_taxonomy_factor'] = new_factor
    return kwargs


def _validate_args_by_ncbi_taxonomy(args: tuple, node_cls: Type[DjangoNode]):
    args = tuple(args)
    for arg in args:
        if 'ncbi_taxonomy' not in arg:
            continue

        _validate_duplicates(value=arg['ncbi_taxonomy'],
                             transformers=[to_int, to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key='ncbi_taxonomy_factor')

    for arg in args:
        if 'ncbi_taxonomy' not in arg:
            continue

        new_factor = _validate_factor(value=arg['ncbi_taxonomy'], transformers=[to_int, to_str, lower, rstrip, lstrip])
        arg['ncbi_taxonomy_factor'] = new_factor

    return args


# ------------------------------------------------
# VALIDATION OF THE PUBMED ID ATTRIBUTE
# ------------------------------------------------
def _validate_kwargs_by_pmid(kwargs: dict, node_cls: Type[DjangoNode], header: str, entity: str):
    kwargs = kwargs.copy()
    _validate_duplicates(value=kwargs['pmid'],
                         transformers=[to_int, to_str, lower, rstrip, lstrip],
                         node_cls=node_cls,
                         key='pmid_factor')

    idx = _get_last_idx(node_cls) + 1
    new_id = protrend_id_encoder(header=header, entity=entity, integer=idx)
    kwargs['protrend_id'] = new_id

    new_factor = _validate_factor(value=kwargs['pmid'], transformers=[to_int, to_str, lower, rstrip, lstrip])
    kwargs['pmid_factor'] = new_factor
    return kwargs


def _validate_args_by_pmid(args: tuple, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    for arg in args:
        _validate_duplicates(value=arg['pmid'],
                             transformers=[to_int, to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key='pmid_factor')

    idx = _get_last_idx(node_cls) + 1
    for i, arg in enumerate(args):
        i = idx + i
        new_id = protrend_id_encoder(header=header, entity=entity, integer=i)
        arg['protrend_id'] = new_id

        new_factor = _validate_factor(value=arg['pmid'], transformers=[to_int, to_str, lower, rstrip, lstrip])
        arg['pmid_factor'] = new_factor

    return args


# ------------------------------------------------
# VALIDATION OF THE INTERACTION HASH ATTRIBUTE
# ------------------------------------------------
def _build_interaction_hash(kwargs: dict) -> str:
    # order matters
    organism = kwargs.get('organism', '')
    regulator = kwargs.get('regulator', '')
    gene = kwargs.get('gene', '')
    tfbs = kwargs.get('tfbs', '')
    effector = kwargs.get('effector', '')
    regulatory_effect = kwargs.get('regulatory_effect', '')
    return protrend_hash([organism, regulator, gene, tfbs, effector, regulatory_effect])


def _validate_kwargs_by_interaction_hash(kwargs: dict, node_cls: Type[DjangoNode], header: str, entity: str):
    kwargs = kwargs.copy()
    interaction_hash = _build_interaction_hash(kwargs)
    return _validate_kwargs_by_hash(kwargs=kwargs, factor='interaction_hash', value=interaction_hash, node_cls=node_cls,
                                    header=header, entity=entity)


def _validate_args_by_interaction_hash(args: tuple, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    hashes = []
    for arg in args:
        interaction_hash = _build_interaction_hash(arg)
        hashes.append(interaction_hash)

    return _validate_args_by_hash(args=args, factor='interaction_hash', values=hashes, node_cls=node_cls,
                                  header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE SITE HASH ATTRIBUTE
# ------------------------------------------------
def _build_site_hash(kwargs: dict) -> str:
    # order matters
    organism = kwargs.get('organism', '')
    sequence = kwargs.get('sequence', '')
    strand = kwargs.get('strand', '')
    start = to_str(kwargs.get('start', ''))
    stop = to_str(kwargs.get('stop', ''))
    length = to_str(kwargs.get('length', ''))
    return protrend_hash([organism, sequence, strand, start, stop, length])


def _validate_kwargs_by_site_hash(kwargs: dict, node_cls: Type[DjangoNode], header: str, entity: str):
    kwargs = kwargs.copy()
    site_hash = _build_site_hash(kwargs)
    return _validate_kwargs_by_hash(kwargs=kwargs, factor='site_hash', value=site_hash, node_cls=node_cls,
                                    header=header, entity=entity)


def _validate_args_by_site_hash(args: tuple, node_cls: Type[DjangoNode], header: str, entity: str):
    args = tuple(args)
    hashes = []
    for arg in args:
        site_hash = _build_site_hash(arg)
        hashes.append(site_hash)

    return _validate_args_by_hash(args=args, factor='site_hash', values=hashes, node_cls=node_cls,
                                  header=header, entity=entity)