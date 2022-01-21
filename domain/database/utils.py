from typing import Union, List


def protrend_id_encoder(header: str, entity: str, integer: Union[str, int]) -> str:
    integer = int(integer)

    return f'{header}.{entity}.{integer:07}'


def protrend_id_decoder(protrend_id: str) -> int:
    prt, entity, integer = protrend_id.split('.')

    return int(integer)


def protrend_identifiers_batch(header: str, entity: str, start: Union[str, int], size: int) -> List[str]:

    return [protrend_id_encoder(header, entity, i)
            for i in range(start, start + size)]
