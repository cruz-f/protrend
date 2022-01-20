from typing import List, Dict, Any

from data import Operon
import domain.model_api as mapi


def create_operons(*operons: Dict[str, Any]) -> List[Operon]:
    """
    Create operons into the database
    """
    return mapi.create_objects(Operon, *operons)


def delete_operons(*operons: Operon):
    """
    Delete operons from the database
    """
    return mapi.delete_objects(*operons)


def create_operon(**kwargs) -> Operon:
    """
    Create a given operon into the database according to the parameters
    """
    return mapi.create_object(Operon, **kwargs)


def update_operon(operon: Operon, **kwargs) -> Operon:
    """
    Update the operon into the database according to the parameters
    """
    return mapi.update_object(operon, **kwargs)


def delete_operon(operon: Operon) -> Operon:
    """
    Delete the operon from the database
    """
    return mapi.delete_object(operon)
