from typing import List, Dict, Any

from rest_framework import status

from data import Gene
import domain.model_api as mapi
from domain.database._validate import (_validate_args_by_locus_tag, _validate_kwargs_by_locus_tag,
                                       _validate_args_by_uniprot_accession, _validate_kwargs_by_uniprot_accession)
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'GEN'


def create_genes(*genes: Dict[str, Any]) -> List[Gene]:
    """
    Create genes into the database
    """
    genes = _validate_args_by_locus_tag(args=genes, node_cls=Gene, header=_HEADER, entity=_ENTITY)
    genes = _validate_args_by_uniprot_accession(args=genes, node_cls=Gene)
    return mapi.create_objects(Gene, *genes)


def delete_genes(*genes: Gene):
    """
    Delete genes from the database
    """
    return mapi.delete_objects(*genes)


def create_gene(**kwargs) -> Gene:
    """
    Create a given gene into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_locus_tag(kwargs=kwargs, node_cls=Gene, header=_HEADER, entity=_ENTITY)
    kwargs = _validate_kwargs_by_uniprot_accession(kwargs=kwargs, node_cls=Gene)
    return mapi.create_object(Gene, **kwargs)


def update_gene(gene: Gene, **kwargs) -> Gene:
    """
    Update the gene into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'locus_tag' in kwargs:
        _validate_kwargs_by_locus_tag(kwargs=kwargs, node_cls=Gene, header=_HEADER, entity=_ENTITY)

    if 'uniprot_accession' in kwargs:
        _validate_kwargs_by_uniprot_accession(kwargs=kwargs, node_cls=Gene)

    return mapi.update_object(gene, **kwargs)


def delete_gene(gene: Gene) -> Gene:
    """
    Delete the gene from the database
    """
    return mapi.delete_object(gene)
