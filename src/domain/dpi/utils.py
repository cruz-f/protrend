from functools import wraps
from typing import Union, Callable

from neo4j.exceptions import DriverError, Neo4jError
from neomodel import NeomodelException
from rest_framework import status

from exceptions import ProtrendException


def protrend_id_encoder(header: str, entity: str, integer: Union[str, int]) -> str:
    integer = int(integer)

    return f'{header}.{entity}.{integer:07}'


def protrend_id_decoder(protrend_id: str) -> int:
    prt, entity, integer = protrend_id.split('.')

    return int(integer)


def raise_exception(fn: Callable):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except (AttributeError, IndexError, NeomodelException, Neo4jError, DriverError):
            raise ProtrendException(detail='ProTReND database is currently unavailable. '
                                           'Please try again later or contact the support team',
                                    code='service unavailable',
                                    status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return wrapper
