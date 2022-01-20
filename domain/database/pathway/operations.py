from typing import List, Dict, Any

from data import Pathway
import domain.model_api as mapi


def create_pathways(*pathways: Dict[str, Any]) -> List[Pathway]:
    """
    Create pathways into the database
    """
    return mapi.create_objects(Pathway, *pathways)


def delete_pathways(*pathways: Pathway):
    """
    Delete pathways from the database
    """
    return mapi.delete_objects(*pathways)


def create_pathway(**kwargs) -> Pathway:
    """
    Create a given pathway into the database according to the parameters
    """
    return mapi.create_object(Pathway, **kwargs)


def update_pathway(pathway: Pathway, **kwargs) -> Pathway:
    """
    Update the pathway into the database according to the parameters
    """
    return mapi.update_object(pathway, **kwargs)


def delete_pathway(pathway: Pathway) -> Pathway:
    """
    Delete the pathway from the database
    """
    return mapi.delete_object(pathway)
