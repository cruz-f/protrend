from typing import Callable, List, Type, Union

from django_neomodel import DjangoNode
from rest_framework import status

from exceptions import ProtrendException
from transformers import apply_transformers, to_int, to_str, lower, rstrip, lstrip, protrend_hash
from domain.dpi.queries import get_last_object, get_object
from domain.dpi.utils import protrend_id_decoder, protrend_id_encoder


def _get_last_idx(node_cls: Type[DjangoNode]) -> int:
    last_obj = get_last_object(node_cls)

    if last_obj:
        return protrend_id_decoder(last_obj.protrend_id)
    else:
        return 0


def _transform_factor(value: str, transformers: List[Callable]):
    return apply_transformers(value, *transformers)


def _build_interaction_hash(kwargs: dict) -> str:
    # order matters
    organism = kwargs.get('organism', '')
    regulator = kwargs.get('regulator', '')
    gene = kwargs.get('gene', '')
    tfbs = kwargs.get('tfbs', '')
    effector = kwargs.get('effector', '')
    regulatory_effect = kwargs.get('regulatory_effect', '')
    return protrend_hash([organism, regulator, gene, tfbs, effector, regulatory_effect])


def _build_site_hash(kwargs: dict) -> str:
    # order matters
    organism = kwargs.get('organism', '')
    sequence = kwargs.get('sequence', '')
    strand = kwargs.get('strand', '')
    start = to_str(kwargs.get('start', ''))
    stop = to_str(kwargs.get('stop', ''))
    length = to_str(kwargs.get('length', ''))
    return protrend_hash([organism, sequence, strand, start, stop, length])


# ------------------------------------------------
# VALIDATION OF THE DATABASE UNIQUE CONSTRAINS
# ------------------------------------------------
def duplicate_validation(value: str, transformers: List[Callable], node_cls: Type[DjangoNode], key: str):
    value = apply_transformers(value, *transformers)
    obj = get_object(node_cls, **{key: value})
    if obj is not None:
        raise ProtrendException(detail=f'Duplicated issue. There is a similar entry in the database with this {value} '
                                       f'value. Please check the following protrend_id: {obj.protrend_id}.',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)


# ------------------------------------------------
# VALIDATION OF UNIQUENESS BY LOWER AND STRIP
# ------------------------------------------------
def lower_strip_validation(values: tuple, factor: str, node_cls: Type[DjangoNode], header: str, entity: str):
    for value in values:
        duplicate_validation(value=value[factor],
                             transformers=[to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key=f'{factor}_factor')

    idx = _get_last_idx(node_cls) + 1
    for i, value in enumerate(values):
        i = idx + i
        new_id = protrend_id_encoder(header=header, entity=entity, integer=i)
        value['protrend_id'] = new_id

        new_factor = _transform_factor(value=value[factor], transformers=[to_str, lower, rstrip, lstrip])
        value[f'{factor}_factor'] = new_factor

    return values


# ------------------------------------------------
# VALIDATION OF UNIQUENESS BY HASH
# ------------------------------------------------
def hash_validation(args: tuple,
                    factor: str,
                    values: List[str],
                    node_cls: Type[DjangoNode],
                    header: str,
                    entity: str):
    for arg, value in zip(args, values):
        duplicate_validation(value=value,
                             transformers=[to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key=f'{factor}_factor')

    idx = _get_last_idx(node_cls) + 1
    for i, (arg, value) in enumerate(zip(args, values)):
        i = idx + i
        new_id = protrend_id_encoder(header=header, entity=entity, integer=i)
        arg['protrend_id'] = new_id

        arg[factor] = value

        new_factor = _transform_factor(value=value, transformers=[to_str, lower, rstrip, lstrip])
        arg[f'{factor}_factor'] = new_factor

    return args


# ------------------------------------------------
# VALIDATION OF THE NAME ATTRIBUTE
# ------------------------------------------------
def name_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode], header: str, entity: str):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    return lower_strip_validation(values=values, factor='name', node_cls=node_cls, header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE LOCUS TAG ATTRIBUTE
# ------------------------------------------------
def locus_tag_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode], header: str, entity: str):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    return lower_strip_validation(values=values, factor='locus_tag', node_cls=node_cls, header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE UNIPROT ACCESSION ATTRIBUTE
# ------------------------------------------------
def uniprot_accession_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode]):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    for arg in values:
        if 'uniprot_accession' not in arg:
            continue

        duplicate_validation(value=arg['uniprot_accession'],
                             transformers=[to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key='uniprot_accession_factor')

    for arg in values:
        if 'uniprot_accession' not in arg:
            continue

        new_factor = _transform_factor(value=arg['uniprot_accession'], transformers=[to_str, lower, rstrip, lstrip])
        arg['uniprot_accession_factor'] = new_factor

    return values


# ------------------------------------------------
# VALIDATION OF THE OPERON DB ID ATTRIBUTE
# ------------------------------------------------
def operon_db_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode], header: str, entity: str):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    return lower_strip_validation(values=values, factor='operon_db_id', node_cls=node_cls, header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE NCBI TAXONOMY ATTRIBUTE
# ------------------------------------------------
def ncbi_taxonomy_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode]):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    for value in values:
        if 'ncbi_taxonomy' not in value:
            continue

        duplicate_validation(value=value['ncbi_taxonomy'],
                             transformers=[to_int, to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key='ncbi_taxonomy_factor')

    for value in values:
        if 'ncbi_taxonomy' not in value:
            continue

        new_factor = _transform_factor(value=value['ncbi_taxonomy'],
                                       transformers=[to_int, to_str, lower, rstrip, lstrip])
        value['ncbi_taxonomy_factor'] = new_factor

    return values


# ------------------------------------------------
# VALIDATION OF THE PUBMED ID ATTRIBUTE
# ------------------------------------------------
def pmid_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode], header: str, entity: str):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    for arg in values:
        duplicate_validation(value=arg['pmid'],
                             transformers=[to_int, to_str, lower, rstrip, lstrip],
                             node_cls=node_cls,
                             key='pmid_factor')

    idx = _get_last_idx(node_cls) + 1
    for i, arg in enumerate(values):
        i = idx + i
        new_id = protrend_id_encoder(header=header, entity=entity, integer=i)
        arg['protrend_id'] = new_id

        new_factor = _transform_factor(value=arg['pmid'], transformers=[to_int, to_str, lower, rstrip, lstrip])
        arg['pmid_factor'] = new_factor

    return values


# ------------------------------------------------
# VALIDATION OF THE INTERACTION HASH ATTRIBUTE
# ------------------------------------------------
def interaction_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode], header: str, entity: str):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    hashes = []
    for arg in values:
        interaction_hash = _build_interaction_hash(arg)
        hashes.append(interaction_hash)

    return hash_validation(args=values, factor='interaction_hash', values=hashes, node_cls=node_cls,
                           header=header, entity=entity)


# ------------------------------------------------
# VALIDATION OF THE SITE HASH ATTRIBUTE
# ------------------------------------------------
def binding_site_validation(values: Union[tuple, dict], node_cls: Type[DjangoNode], header: str, entity: str):
    if isinstance(values, dict):
        values = values.copy()
        values = (values,)

    else:
        values = tuple(values)

    hashes = []
    for arg in values:
        site_hash = _build_site_hash(arg)
        hashes.append(site_hash)

    return hash_validation(args=values, factor='site_hash', values=hashes, node_cls=node_cls,
                           header=header, entity=entity)
