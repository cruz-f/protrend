from typing import List, Dict, Any

from data import Evidence
import domain.model_api as mapi


def create_evidences(*evidences: Dict[str, Any]) -> List[Evidence]:
    """
    Create evidences into the database
    """
    return mapi.create_objects(Evidence, *evidences)


def delete_evidences(*evidences: Evidence):
    """
    Delete evidences from the database
    """
    return mapi.delete_objects(*evidences)


def create_evidence(**kwargs) -> Evidence:
    """
    Create a given evidence into the database according to the parameters
    """
    return mapi.create_object(Evidence, **kwargs)


def update_evidence(evidence: Evidence, **kwargs) -> Evidence:
    """
    Update the evidence into the database according to the parameters
    """
    return mapi.update_object(evidence, **kwargs)


def delete_evidence(evidence: Evidence) -> Evidence:
    """
    Delete the evidence from the database
    """
    return mapi.delete_object(evidence)
