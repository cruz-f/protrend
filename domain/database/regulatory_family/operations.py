from typing import List, Dict, Any

from data import RegulatoryFamily
import domain.model_api as mapi


def create_rfams(*rfams: Dict[str, Any]) -> List[RegulatoryFamily]:
    """
    Create rfams into the database
    """
    return mapi.create_objects(RegulatoryFamily, *rfams)


def delete_rfams(*rfams: RegulatoryFamily):
    """
    Delete rfams from the database
    """
    return mapi.delete_objects(*rfams)


def create_rfam(**kwargs) -> RegulatoryFamily:
    """
    Create a given rfam into the database according to the parameters
    """
    return mapi.create_object(RegulatoryFamily, **kwargs)


def update_rfam(rfam: RegulatoryFamily, **kwargs) -> RegulatoryFamily:
    """
    Update the rfam into the database according to the parameters
    """
    return mapi.update_object(rfam, **kwargs)


def delete_rfam(rfam: RegulatoryFamily) -> RegulatoryFamily:
    """
    Delete the rfam from the database
    """
    return mapi.delete_object(rfam)
