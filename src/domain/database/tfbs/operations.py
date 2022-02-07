from typing import List, Dict, Any

from rest_framework import status

import domain.model_api as mapi
from data import TFBS, Organism
from domain.database._validate import _validate_args_by_site_hash, _validate_kwargs_by_site_hash
from exceptions import ProtrendException

_HEADER = 'PRT'
_ENTITY = 'TBS'


def create_binding_sites(*binding_sites: Dict[str, Any]) -> List[TFBS]:
    """
    Create binding_sites into the database
    """
    from domain.database.organism.queries import get_organism_by_id

    organisms = []
    for site in binding_sites:
        organism = site['organism']
        obj = get_organism_by_id(organism)
        if obj is None:
            raise ProtrendException(detail=f'The submitted {organism} protrend id for the property organism '
                                           f'was not found in the database.',
                                    code='create or update error',
                                    status=status.HTTP_400_BAD_REQUEST)
        organisms.append(obj)

    binding_sites = _validate_args_by_site_hash(args=binding_sites, node_cls=TFBS, header=_HEADER, entity=_ENTITY)
    objs = mapi.create_objects(TFBS, *binding_sites)

    for obj, organism_obj in zip(objs, organisms):
        try:
            create_binding_site_relationships(binding_site=obj, organism=organism_obj)

        except ProtrendException:
            # if something goes wrong the interaction must be deleted
            delete_binding_site(obj)

    return objs


def delete_binding_sites(*binding_sites: TFBS):
    """
    Delete binding_sites from the database
    """
    for binding_site in binding_sites:
        delete_binding_site(binding_site)


def create_binding_site(**kwargs) -> TFBS:
    """
    Create a given binding_site into the database according to the parameters
    """
    from domain.database.organism.queries import get_organism_by_id

    organism = kwargs['organism']
    organism_obj = get_organism_by_id(organism)
    if organism_obj is None:
        raise ProtrendException(detail=f'The submitted {organism} protrend id for the property organism '
                                       f'was not found in the database.',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    kwargs = _validate_kwargs_by_site_hash(kwargs=kwargs, node_cls=TFBS, header=_HEADER, entity=_ENTITY)
    obj = mapi.create_object(TFBS, **kwargs)

    try:
        create_binding_site_relationships(binding_site=obj, organism=organism_obj)

    except ProtrendException:
        # if something goes wrong the interaction must be deleted
        delete_binding_site(obj)
    return obj


def update_binding_site(_: TFBS, **kwargs):
    """
    Update the binding_site into the database according to the parameters
    """
    raise ProtrendException(detail=f'TFBS update operation is not supported. '
                                   f'Please create a new binding site',
                            code='create or update error',
                            status=status.HTTP_400_BAD_REQUEST)


def delete_binding_site(binding_site: TFBS) -> TFBS:
    """
    Delete the binding_site from the database
    """
    from domain.database.regulatory_interaction.operations import delete_interactions

    # first let's delete interactions associated with the organism
    interactions = mapi.get_related_objects(binding_site, 'regulatory_interaction')
    delete_interactions(*interactions)

    return mapi.delete_object(binding_site)


def create_binding_site_relationships(binding_site: TFBS, organism: Organism):
    """
    Create a relationship between binding_site and organism
    """
    mapi.create_or_none(source_obj=binding_site, target='data_organism', target_obj=organism)
    mapi.create_or_none(source_obj=organism, target='tfbs', target_obj=binding_site)
