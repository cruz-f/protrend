from typing import List, Dict, Any

from data import TFBS
import domain.model_api as mapi


def create_biding_sites(*biding_sites: Dict[str, Any]) -> List[TFBS]:
    """
    Create biding_sites into the database
    """
    return mapi.create_objects(TFBS, *biding_sites)


def delete_biding_sites(*biding_sites: TFBS):
    """
    Delete biding_sites from the database
    """
    return mapi.delete_objects(*biding_sites)


def create_biding_site(**kwargs) -> TFBS:
    """
    Create a given biding_site into the database according to the parameters
    """
    return mapi.create_object(TFBS, **kwargs)


def update_biding_site(biding_site: TFBS, **kwargs) -> TFBS:
    """
    Update the biding_site into the database according to the parameters
    """
    return mapi.update_object(biding_site, **kwargs)


def delete_biding_site(biding_site: TFBS) -> TFBS:
    """
    Delete the biding_site from the database
    """
    return mapi.delete_object(biding_site)
