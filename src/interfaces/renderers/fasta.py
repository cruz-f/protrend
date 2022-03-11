from io import StringIO
from typing import List

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from rest_framework import renderers


class FastaRenderer(renderers.BaseRenderer):
    media_type = 'text/fasta'
    format = 'fasta'
    filename = 'protrend_data.fasta'

    @staticmethod
    def build_regulator_records(sites: List[dict],
                                protrend_id: str,
                                locus_tag: str,
                                uniprot_acc: str) -> List[SeqRecord]:
        records = []
        for site in sites:
            site_protrend_id = site.get('protrend_id', '')
            sequence = site.get('sequence', '')
            strand = site.get('strand', '')
            start = site.get('start', '')
            stop = site.get('stop', '')

            if not sequence:
                continue

            description = 'ProTReND binding-site sequence of regulator ' \
                          f'{protrend_id}-{locus_tag}-{uniprot_acc} and genomic coordinates: {strand}-{start}-{stop}'

            seq = Seq(sequence)
            record = SeqRecord(seq=seq,
                               id=site_protrend_id,
                               name=site_protrend_id,
                               description=description)
            records.append(record)

        return records

    @staticmethod
    def build_organism_records(sites: List[dict],
                               protrend_id: str,
                               name: str,
                               ncbi_taxonomy: str) -> List[SeqRecord]:
        records = []
        for site in sites:
            site_protrend_id = site.get('protrend_id', '')
            sequence = site.get('sequence', '')
            strand = site.get('strand', '')
            start = site.get('start', '')
            stop = site.get('stop', '')

            if not sequence:
                continue

            description = 'ProTReND binding-site sequence of organism ' \
                          f'{protrend_id}-{name}-{ncbi_taxonomy} and genomic coordinates: {strand}-{start}-{stop}'

            seq = Seq(sequence)
            record = SeqRecord(seq=seq,
                               id=site_protrend_id,
                               name=site_protrend_id,
                               description=description)
            records.append(record)

        return records

    def render(self, data, media_type=None, renderer_context=None):
        if not data:
            return ''

        sites = data.get('tfbs', [])

        if 'ncbi_taxonomy' in data:
            protrend_id = data.get('protrend_id', '')
            name = data.get('name', '')
            ncbi_taxonomy = data.get('ncbi_taxonomy', '')
            records = self.build_organism_records(sites, protrend_id, name, ncbi_taxonomy)

        elif 'mechanism' in data:
            protrend_id = data.get('protrend_id', '')
            locus_tag = data.get('locus_tag', '')
            uniprot_acc = data.get('uniprot_acc', '')
            records = self.build_regulator_records(sites, protrend_id, locus_tag, uniprot_acc)

        else:
            records = []

        buffer = StringIO()
        SeqIO.write(records, buffer, "fasta")
        return buffer.getvalue()
