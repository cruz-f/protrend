import re
from io import StringIO

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio.SeqRecord import SeqRecord
from rest_framework import renderers

from constants import FORWARD, REVERSE, UNKNOWN

PROTREND_ORG_IDENTIFIER_PATTERN = re.compile(r'PRT\.ORG\.\d+')


def _get_sequence(data, molecule_type):
    if molecule_type == 'DNA':
        sequence = data.get('gene_sequence', '')

    elif molecule_type == 'protein':
        sequence = data.get('protein_sequence', '')

    else:
        sequence = ''

    if not sequence:
        sequence = ''

    return sequence


def _get_organism(data):
    organism = data.get('organism', [''])[0]

    match = PROTREND_ORG_IDENTIFIER_PATTERN.search(organism)

    if match:
        return match.group()

    return


def _get_description(protrend_id, organism, mechanism):
    if mechanism:
        return f'Regulator {protrend_id} in {organism}'

    return f'Gene {protrend_id} in {organism}'


def _get_strand(strand, molecule_type):
    if strand == FORWARD:
        return 1

    elif strand == REVERSE:
        return -1

    elif strand == UNKNOWN and molecule_type == 'DNA':

        return 0

    return


def _get_dbxrefs(data, protrend_id):
    dbxrefs = [f'ProTReND:{protrend_id}']

    refs = {'uniprot_accession': 'UniProtKB',
            'ncbi_gene': 'NCBIGene',
            'ncbi_protein': 'NCBIProtein',
            'genbank_accession': 'GenBank',
            'refseq_accession': 'RefSeq'}

    for key, val in refs.items():
        ref = data.get(key)
        if ref:
            dbxrefs.append(f'{val}:{ref}')

    return dbxrefs


def _get_annotations(molecule_type, date, source, organism,
                     name, locus_tag, synonyms, function):
    return {'molecule_type': molecule_type,
            'date': date,
            'source': source,
            'organism': organism,
            'gene': [name],
            'locus_tag': [locus_tag],
            'synonyms': synonyms,
            'product': [function]}


def _get_feature_location(sequence, start, end, strand):
    return FeatureLocation(0, len(sequence), strand=strand)


def _get_feature(protrend_id, feature_sequence, feature_start, feature_stop, feature_strand,
                 locus_tag, name, synonyms, function, mechanism, dbxrefs):
    location = _get_feature_location(feature_sequence, feature_start, feature_stop, feature_strand)

    qualifiers = {'gene': [name],
                  'locus_tag': [locus_tag],
                  'synonyms': synonyms,
                  'product': [function],
                  'db_xref': dbxrefs}

    if mechanism:
        qualifiers['mechanism'] = [mechanism]

    return SeqFeature(id=protrend_id,
                      location=location,
                      type='CDS',
                      strand=feature_strand,
                      qualifiers=qualifiers)


def build_gnb_record(data, molecule_type, date):
    """
    Builds a GenBank record from a dictionary of data.
    """
    protrend_id = data.get('protrend_id')

    # regulator only
    mechanism = data.get('mechanism')

    strand = _get_strand(data.get('strand'), molecule_type=molecule_type)
    start = data.get('start')
    stop = data.get('stop')

    locus_tag = data.get('locus_tag')
    name = data.get('name', '')
    synonyms = data.get('synonyms', [])
    function = data.get('function')

    sequence = _get_sequence(data, molecule_type=molecule_type)

    organism = _get_organism(data)

    description = _get_description(protrend_id=protrend_id, organism=organism, mechanism=mechanism)

    annotations = _get_annotations(molecule_type=molecule_type,
                                   date=date,
                                   source=organism,
                                   organism=organism,
                                   name=name,
                                   locus_tag=locus_tag,
                                   synonyms=synonyms,
                                   function=function)

    dbxrefs = _get_dbxrefs(data, protrend_id)

    seq_feature = _get_feature(protrend_id=protrend_id,
                               feature_sequence=sequence,
                               feature_start=start,
                               feature_stop=stop,
                               feature_strand=strand,
                               locus_tag=locus_tag,
                               name=name,
                               synonyms=synonyms,
                               function=function,
                               mechanism=mechanism,
                               dbxrefs=dbxrefs)

    record = SeqRecord(seq=Seq(sequence),
                       id=protrend_id,
                       name=protrend_id,
                       description=description,
                       annotations=annotations,
                       dbxrefs=dbxrefs,
                       features=[seq_feature])

    return record


class NucleotideGenBankRenderer(renderers.BaseRenderer):
    media_type = 'text/gnb'
    format = 'gbff'
    filename = 'protrend_data.gbff'

    molecule_type = 'DNA'
    date = '27-AUG-2022'

    def render(self, data, media_type=None, renderer_context=None):
        if not data:
            return ''

        protrend_id = data.get('protrend_id', '')

        if protrend_id.startswith('PRT.REG.'):
            record = build_gnb_record(data, molecule_type=self.molecule_type, date=self.date)
            records = [record]

        elif protrend_id.startswith('PRT.GEN.'):
            record = build_gnb_record(data, molecule_type=self.molecule_type, date=self.date)
            records = [record]

        else:
            records = []

        buffer = StringIO()
        SeqIO.write(records, buffer, "genbank")
        return buffer.getvalue()


class AminoAcidGenBankRenderer(NucleotideGenBankRenderer):
    media_type = 'text/gnb'
    format = 'gpff'
    filename = 'protrend_data.gpff'

    molecule_type = 'protein'
