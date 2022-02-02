from typing import List, Dict, Any

from rest_framework import status

import domain.model_api as mapi
from data import Operon, Gene
from domain.database import get_gene_by_id
from domain.database._validate import _validate_kwargs_by_operon_db_id, _validate_args_by_operon_db_id
from exceptions import ProtrendException

_HEADER = 'PRT'
_ENTITY = 'OPN'


def create_operons(*operons: Dict[str, Any]) -> List[Operon]:
    """
    Create operons into the database
    """
    operons = _validate_args_by_operon_db_id(args=operons, node_cls=Operon, header=_HEADER, entity=_ENTITY)
    objs = mapi.create_objects(Operon, *operons)

    for obj in objs:
        genes = [get_gene_by_id(gene) for gene in obj.genes]
        create_operon_relationships(operon=obj, genes=genes)

    return objs


def delete_operons(*operons: Operon):
    """
    Delete operons from the database
    """
    return mapi.delete_objects(*operons)


def create_operon(**kwargs) -> Operon:
    """
    Create a given operon into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_operon_db_id(kwargs=kwargs, node_cls=Operon, header=_HEADER, entity=_ENTITY)
    obj = mapi.create_object(Operon, **kwargs)
    genes = [get_gene_by_id(gene) for gene in obj.genes]
    create_operon_relationships(operon=obj, genes=genes)
    return obj


def update_operon(operon: Operon, **kwargs) -> Operon:
    """
    Update the operon into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'operon_db_id' in kwargs:
        operon_db_id = kwargs['operon_db_id']
        if operon_db_id != operon.operon_db_id:
            kwargs = _validate_kwargs_by_operon_db_id(kwargs=kwargs, node_cls=Operon, header=_HEADER, entity=_ENTITY)
            kwargs.pop('protrend_id')

    return mapi.update_object(operon, **kwargs)


def delete_operon(operon: Operon) -> Operon:
    """
    Delete the operon from the database
    """
    return mapi.delete_object(operon)


def create_operon_relationships(operon: Operon, genes: List[Gene]):
    """
    Create a relationship between operon and genes
    """
    for gene in genes:
        mapi.create_relationship(source_obj=operon, target='gene', target_obj=gene)
        mapi.create_relationship(source_obj=gene, target='operon', target_obj=operon)
