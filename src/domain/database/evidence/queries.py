from typing import List

from data import Evidence, TFBS, RegulatoryInteraction
import domain.model_api as mapi


def get_evidences() -> List[Evidence]:
    """
    Get evidences list from database
    """
    return mapi.get_objects(Evidence)


def filter_evidences(*args, **kwargs) -> List[Evidence]:
    """
    Get and filter evidences from database
    """
    return mapi.filter_objects(Evidence, *args, **kwargs)


def order_by_evidences(*fields) -> List[Evidence]:
    """
    Get and order by evidences from database
    """
    return mapi.order_by_objects(Evidence, *fields)


def order_evidences_by_id() -> List[Evidence]:
    """
    Get and order by evidences by protrend identifier from database
    """
    return mapi.order_by_objects(Evidence, 'protrend_id')


def get_evidence(**kwargs) -> Evidence:
    """
    Get a given evidence from database
    """
    return mapi.get_object(Evidence, **kwargs)


def get_evidence_by_id(protrend_id: str) -> Evidence:
    """
    Get a given evidence from database using the protrend identifier
    """
    return mapi.get_object(Evidence, protrend_id=protrend_id)


def get_last_evidence() -> Evidence:
    """
    Get the last evidence from database using the protrend identifier
    """
    return mapi.get_last_object(Evidence, 'protrend_id')


def get_evidence_binding_sites(protrend_id: str) -> List[TFBS]:
    """
    Get binding sites connected with this evidence
    """
    obj = get_evidence_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'tfbs')


def get_evidence_interactions(protrend_id: str) -> List[RegulatoryInteraction]:
    """
    Get interactions connected with this evidence
    """
    obj = get_evidence_by_id(protrend_id)
    return mapi.get_related_objects(obj, 'regulatory_interaction')
