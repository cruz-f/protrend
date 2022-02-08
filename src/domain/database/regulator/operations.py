from typing import List, Dict, Any

from rest_framework import status

from data import Regulator
import domain.model_api as mapi
from domain.database._validate import (_validate_args_by_locus_tag, _validate_args_by_uniprot_accession,
                                       _validate_kwargs_by_locus_tag, _validate_kwargs_by_uniprot_accession)
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'REG'


def create_regulators(*regulators: Dict[str, Any]) -> List[Regulator]:
    """
    Create regulators into the database
    """
    regulators = _validate_args_by_locus_tag(args=regulators, node_cls=Regulator, header=_HEADER, entity=_ENTITY)
    regulators = _validate_args_by_uniprot_accession(args=regulators, node_cls=Regulator)
    return mapi.create_objects(Regulator, *regulators)


def delete_regulators(*regulators: Regulator):
    """
    Delete regulators from the database
    """
    for regulator in regulators:
        delete_regulator(regulator)


def create_regulator(**kwargs) -> Regulator:
    """
    Create a given regulator into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_locus_tag(kwargs=kwargs, node_cls=Regulator, header=_HEADER, entity=_ENTITY)
    kwargs = _validate_kwargs_by_uniprot_accession(kwargs=kwargs, node_cls=Regulator)
    return mapi.create_object(Regulator, **kwargs)


def update_regulator(regulator: Regulator, **kwargs) -> Regulator:
    """
    Update the regulator into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'locus_tag' in kwargs:
        locus_tag = kwargs['locus_tag']
        if locus_tag != regulator.locus_tag:
            kwargs = _validate_kwargs_by_locus_tag(kwargs=kwargs, node_cls=Regulator, header=_HEADER, entity=_ENTITY)
            kwargs.pop('protrend_id')

    if 'uniprot_accession' in kwargs:
        uniprot_accession = kwargs['uniprot_accession']
        if uniprot_accession != regulator.uniprot_accession:
            kwargs = _validate_kwargs_by_uniprot_accession(kwargs=kwargs, node_cls=Regulator)

    return mapi.update_object(regulator, **kwargs)


def delete_regulator(regulator: Regulator) -> Regulator:
    """
    Delete the regulator from the database
    """
    from domain.database.regulatory_interaction.operations import delete_interactions

    # first let's delete interactions associated with the organism
    interactions = mapi.get_related_objects(regulator, 'regulatory_interaction')
    delete_interactions(*interactions)

    return mapi.delete_object(regulator)
