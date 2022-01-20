from typing import List, Dict, Any

from data import Organism
import domain.model_api as mapi


def create_organisms(*organisms: Dict[str, Any]) -> List[Organism]:
    """
    Create organisms into the database
    """
    return mapi.create_objects(Organism, *organisms)


def delete_organisms(*organisms: Organism):
    """
    Delete organisms from the database
    """
    return mapi.delete_objects(*organisms)


def create_organism(**kwargs) -> Organism:
    """
    Create a given organism into the database according to the parameters
    """
    return mapi.create_object(Organism, **kwargs)


def update_organism(organism: Organism, **kwargs) -> Organism:
    """
    Update the organism into the database according to the parameters
    """
    return mapi.update_object(organism, **kwargs)


def delete_organism(organism: Organism) -> Organism:
    """
    Delete the organism from the database
    """
    return mapi.delete_object(organism)
