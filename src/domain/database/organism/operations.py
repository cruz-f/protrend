from typing import List, Dict, Any

from rest_framework import status

import domain.model_api as mapi
from data import Organism
from domain.database._validate import (_validate_args_by_name, _validate_kwargs_by_name,
                                       _validate_kwargs_by_ncbi_taxonomy, _validate_args_by_ncbi_taxonomy)
from exceptions import ProtrendException

_HEADER = 'PRT'
_ENTITY = 'ORG'


def create_organisms(*organisms: Dict[str, Any]) -> List[Organism]:
    """
    Create organisms into the database
    """
    organisms = _validate_args_by_name(args=organisms, node_cls=Organism, header=_HEADER, entity=_ENTITY)
    organisms = _validate_args_by_ncbi_taxonomy(args=organisms, node_cls=Organism)
    return mapi.create_objects(Organism, *organisms)


def delete_organisms(*organisms: Organism):
    """
    Delete organisms from the database
    """
    for organism in organisms:
        delete_organism(organism)


def create_organism(**kwargs) -> Organism:
    """
    Create a given organism into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Organism, header=_HEADER, entity=_ENTITY)
    kwargs = _validate_kwargs_by_ncbi_taxonomy(kwargs=kwargs, node_cls=Organism)
    return mapi.create_object(Organism, **kwargs)


def update_organism(organism: Organism, **kwargs) -> Organism:
    """
    Update the organism into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'name' in kwargs:
        name = kwargs['name']
        if name != organism.name:
            kwargs = _validate_kwargs_by_name(kwargs=kwargs, node_cls=Organism, header=_HEADER, entity=_ENTITY)
            kwargs.pop('protrend_id')

    if 'ncbi_taxonomy' in kwargs:
        ncbi_taxonomy = kwargs['ncbi_taxonomy']
        if ncbi_taxonomy != organism.ncbi_taxonomy:
            kwargs = _validate_kwargs_by_ncbi_taxonomy(kwargs=kwargs, node_cls=Organism)

    return mapi.update_object(organism, **kwargs)


def delete_organism(organism: Organism) -> Organism:
    """
    Delete the organism from the database
    """
    from domain.database.regulator.operations import delete_regulators
    from domain.database.gene.operations import delete_genes
    from domain.database.tfbs.operations import delete_binding_sites
    from domain.database.regulatory_interaction.operations import delete_interactions

    # first let's delete the regulator, genes, binding sites and interactions associated with the organism
    regulators = mapi.get_related_objects(organism, 'regulator')
    delete_regulators(*regulators)

    genes = mapi.get_related_objects(organism, 'gene')
    delete_genes(*genes)

    binding_sites = mapi.get_related_objects(organism, 'tfbs')
    delete_binding_sites(*binding_sites)

    interactions = mapi.get_related_objects(organism, 'regulatory_interactions')
    delete_interactions(*interactions)

    return mapi.delete_object(organism)
