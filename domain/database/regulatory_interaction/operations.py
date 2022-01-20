from typing import List, Dict, Any

from data import RegulatoryInteraction
import domain.model_api as mapi


def create_interactions(*interactions: Dict[str, Any]) -> List[RegulatoryInteraction]:
    """
    Create interactions into the database
    """
    return mapi.create_objects(RegulatoryInteraction, *interactions)


def delete_interactions(*interactions: RegulatoryInteraction):
    """
    Delete interactions from the database
    """
    return mapi.delete_objects(*interactions)


def create_interaction(**kwargs) -> RegulatoryInteraction:
    """
    Create a given interaction into the database according to the parameters
    """
    return mapi.create_object(RegulatoryInteraction, **kwargs)


def update_interaction(interaction: RegulatoryInteraction, **kwargs) -> RegulatoryInteraction:
    """
    Update the interaction into the database according to the parameters
    """
    return mapi.update_object(interaction, **kwargs)


def delete_interaction(interaction: RegulatoryInteraction) -> RegulatoryInteraction:
    """
    Delete the interaction from the database
    """
    return mapi.delete_object(interaction)
