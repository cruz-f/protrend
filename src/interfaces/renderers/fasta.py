from io import StringIO

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from rest_framework import renderers


class NucleotideFastaRenderer(renderers.BaseRenderer):
    media_type = 'text/fasta'
    format = 'fna'
    filename = 'protrend_data.fna'

    @staticmethod
    def build_regulator_record(data: dict) -> list:
        """
        It builds regulator fna record
        """
        protrend_id = data.get('protrend_id', '')
        locus_tag = data.get('locus_tag', '')
        name = data.get('name', '')
        uniprot_acc = data.get('uniprot_acc', '')
        mechanism = data.get('mechanism', '')

        sequence = data.get('gene_sequence', '')
        if not sequence:
            sequence = ''
        sequence = Seq(sequence)

        description = f'Regulator {protrend_id}-{locus_tag}-{name}-{uniprot_acc}-{mechanism}'

        record = SeqRecord(seq=sequence,
                           id=protrend_id,
                           name=protrend_id,
                           description=description)
        return [record]

    @staticmethod
    def build_gene_record(data: dict) -> list:
        """
        It builds gene fna record
        """
        protrend_id = data.get('protrend_id', '')
        locus_tag = data.get('locus_tag', '')
        name = data.get('name', '')
        uniprot_acc = data.get('uniprot_acc', '')

        sequence = data.get('gene_sequence', '')
        if not sequence:
            sequence = ''
        sequence = Seq(sequence)

        description = f'Gene {protrend_id}-{locus_tag}-{name}-{uniprot_acc}'

        record = SeqRecord(seq=sequence,
                           id=protrend_id,
                           name=protrend_id,
                           description=description)
        return [record]

    def render(self, data, media_type=None, renderer_context=None):
        if not data:
            return ''

        protrend_id = data.get('protrend_id', '')

        if protrend_id.startswith('PRT.REG.'):
            records = self.build_regulator_record(data)

        elif protrend_id.startswith('PRT.GEN.'):
            records = self.build_gene_record(data)

        else:
            records = []

        buffer = StringIO()
        SeqIO.write(records, buffer, "fasta")
        return buffer.getvalue()


class AminoAcidFastaRenderer(NucleotideFastaRenderer):
    media_type = 'text/fasta'
    format = 'faa'
    filename = 'protrend_data.faa'

    @staticmethod
    def build_regulator_record(data: dict) -> list:
        """
        It builds regulator faa record
        """
        protrend_id = data.get('protrend_id', '')
        locus_tag = data.get('locus_tag', '')
        name = data.get('name', '')
        uniprot_acc = data.get('uniprot_acc', '')
        mechanism = data.get('mechanism', '')

        sequence = data.get('protein_sequence', '')
        if not sequence:
            sequence = 'NA'
        sequence = Seq(sequence)

        description = f'Regulator {protrend_id}-{locus_tag}-{name}-{uniprot_acc}-{mechanism}'

        record = SeqRecord(seq=sequence,
                           id=protrend_id,
                           name=protrend_id,
                           description=description)
        return [record]

    @staticmethod
    def build_gene_record(data: dict) -> list:
        """
        It builds gene faa record
        """
        protrend_id = data.get('protrend_id', '')
        locus_tag = data.get('locus_tag', '')
        name = data.get('name', '')
        uniprot_acc = data.get('uniprot_acc', '')

        sequence = data.get('protein_sequence', '')
        if not sequence:
            sequence = 'NA'
        sequence = Seq(sequence)

        description = f'Gene {protrend_id}-{locus_tag}-{name}-{uniprot_acc}'

        record = SeqRecord(seq=sequence,
                           id=protrend_id,
                           name=protrend_id,
                           description=description)
        return [record]
