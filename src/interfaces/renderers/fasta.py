from io import StringIO
from typing import Union

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from rest_framework import renderers


class FastaRenderer(renderers.BaseRenderer):
    media_type = 'text/fasta'
    format = 'fasta'
    filename = 'protrend_data.fasta'

    @staticmethod
    def build_nested_record(obj: dict) -> Union[SeqRecord, None]:
        tfbs = obj.get('tfbs', {})
        protrend_id = tfbs.get('protrend_id', '')
        sequence = tfbs.get('sequence', '')

        if not sequence:
            return

        regulator = obj.get('regulator', {})
        regulator_protrend_id = regulator.get('protrend_id', '')
        regulator_locus_tag = regulator.get('locus_tag', '')
        regulator_uniprot_acc = regulator.get('uniprot_accession', '')

        description = f'ProTReND sequence of regulator: ' \
                      f'{regulator_protrend_id} - {regulator_locus_tag} - {regulator_uniprot_acc}'

        seq = Seq(sequence)
        record = SeqRecord(seq=seq,
                           id=protrend_id,
                           name=protrend_id,
                           description=description)
        return record

    @staticmethod
    def build_record(obj: dict) -> Union[SeqRecord, None]:
        protrend_id = obj.get('protrend_id', '')
        sequence = obj.get('sequence', '')

        if not sequence:
            return

        description = 'ProTReND binding-site sequence'

        seq = Seq(sequence)
        record = SeqRecord(seq=seq,
                           id=protrend_id,
                           name=protrend_id,
                           description=description)
        return record

    def render(self, data, media_type=None, renderer_context=None):
        if data is None:
            return ''

        if isinstance(data, dict):
            data = data.get('results', [])

        records = []
        for obj in data:
            if 'regulator' and 'tfbs' in obj:
                record = self.build_nested_record(obj)

            else:
                record = self.build_record(obj)

            if record is None:
                continue

            records.append(record)

        buffer = StringIO()
        SeqIO.write(records, buffer, "fasta")
        return buffer.getvalue()
