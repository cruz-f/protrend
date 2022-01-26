from typing import List, Dict, Any

from rest_framework import status

from data import Publication
import domain.model_api as mapi
from domain.database._validate import _validate_args_by_pmid, _validate_kwargs_by_pmid
from exceptions import ProtrendException


_HEADER = 'PRT'
_ENTITY = 'PUB'


def create_publications(*publications: Dict[str, Any]) -> List[Publication]:
    """
    Create publications into the database
    """
    publications = _validate_args_by_pmid(args=publications, node_cls=Publication, header=_HEADER, entity=_ENTITY)
    return mapi.create_objects(Publication, *publications)


def delete_publications(*publications: Publication):
    """
    Delete publications from the database
    """
    return mapi.delete_objects(*publications)


def create_publication(**kwargs) -> Publication:
    """
    Create a given publication into the database according to the parameters
    """
    kwargs = _validate_kwargs_by_pmid(kwargs=kwargs, node_cls=Publication, header=_HEADER, entity=_ENTITY)
    return mapi.create_object(Publication, **kwargs)


def update_publication(publication: Publication, **kwargs) -> Publication:
    """
    Update the publication into the database according to the parameters
    """
    if 'protrend_id' in kwargs:
        raise ProtrendException(detail=f'protrend_id read-only attribute cannot be altered',
                                code='create or update error',
                                status=status.HTTP_400_BAD_REQUEST)

    if 'pmid' in kwargs:
        _validate_kwargs_by_pmid(kwargs=kwargs, node_cls=Publication, header=_HEADER, entity=_ENTITY)

    return mapi.update_object(publication, **kwargs)


def delete_publication(publication: Publication) -> Publication:
    """
    Delete the publication from the database
    """
    return mapi.delete_object(publication)
