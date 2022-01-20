from typing import List, Dict, Any

from data import Publication
import domain.model_api as mapi


def create_publications(*publications: Dict[str, Any]) -> List[Publication]:
    """
    Create publications into the database
    """
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
    return mapi.create_object(Publication, **kwargs)


def update_publication(publication: Publication, **kwargs) -> Publication:
    """
    Update the publication into the database according to the parameters
    """
    return mapi.update_object(publication, **kwargs)


def delete_publication(publication: Publication) -> Publication:
    """
    Delete the publication from the database
    """
    return mapi.delete_object(publication)
