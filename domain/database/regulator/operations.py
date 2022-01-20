from typing import List, Dict, Any

from data import Regulator
import domain.model_api as mapi


def create_regulators(*regulators: Dict[str, Any]) -> List[Regulator]:
    """
    Create regulators into the database
    """
    return mapi.create_objects(Regulator, *regulators)


def delete_regulators(*regulators: Regulator):
    """
    Delete regulators from the database
    """
    return mapi.delete_objects(*regulators)


def create_regulator(**kwargs) -> Regulator:
    """
    Create a given regulator into the database according to the parameters
    """
    return mapi.create_object(Regulator, **kwargs)


def update_regulator(regulator: Regulator, **kwargs) -> Regulator:
    """
    Update the regulator into the database according to the parameters
    """
    return mapi.update_object(regulator, **kwargs)


def delete_regulator(regulator: Regulator) -> Regulator:
    """
    Delete the regulator from the database
    """
    return mapi.delete_object(regulator)
