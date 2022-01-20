from typing import List, Dict, Any

from data import Gene
import domain.model_api as mapi


def create_genes(*genes: Dict[str, Any]) -> List[Gene]:
    """
    Create genes into the database
    """
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
    return mapi.create_object(Gene, **kwargs)


def update_gene(gene: Gene, **kwargs) -> Gene:
    """
    Update the gene into the database according to the parameters
    """
    return mapi.update_object(gene, **kwargs)


def delete_gene(gene: Gene) -> Gene:
    """
    Delete the gene from the database
    """
    return mapi.delete_object(gene)
