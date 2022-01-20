from typing import List, Dict, Any

from data import Effector
import domain.model_api as mapi


def create_effectors(*effectors: Dict[str, Any]) -> List[Effector]:
    """
    Create effectors into the database
    """
    return mapi.create_objects(Effector, *effectors)


def delete_effectors(*effectors: Effector):
    """
    Delete effectors from the database
    """
    return mapi.delete_objects(*effectors)


def create_effector(**kwargs) -> Effector:
    """
    Create a given effector into the database according to the parameters
    """
    return mapi.create_object(Effector, **kwargs)


def update_effector(effector: Effector, **kwargs) -> Effector:
    """
    Update the effector into the database according to the parameters
    """
    return mapi.update_object(effector, **kwargs)


def delete_effector(effector: Effector) -> Effector:
    """
    Delete the effector from the database
    """
    return mapi.delete_object(effector)
