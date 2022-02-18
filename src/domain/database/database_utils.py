from typing import Union


def protrend_id_encoder(header: str, entity: str, integer: Union[str, int]) -> str:
    integer = int(integer)

    return f'{header}.{entity}.{integer:07}'


def protrend_id_decoder(protrend_id: str) -> int:
    prt, entity, integer = protrend_id.split('.')

    return int(integer)
