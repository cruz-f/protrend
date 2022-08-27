from rest_framework import renderers

from application.sequences import make_motif, make_jaspar


class TRANSFACRenderer(renderers.BaseRenderer):
    media_type = 'text/transfac'
    format = 'transfac'
    filename = 'protrend_data.dat'

    def render(self, data, media_type=None, renderer_context=None):

        protrend_id = data.get('protrend_id', '')
        regulator = data.get('regulator', {})
        regulator_protrend_id = regulator.get('protrend_id', '')
        regulator_locus_tag = regulator.get('locus_tag', '')
        regulator_uniprot_accession = regulator.get('uniprot_accession', '')

        aligned_sequences = data.get('sequences', [])

        motif = make_motif(aligned_sequences)
        motif.id = protrend_id
        motif.name = f'Motif {protrend_id} for regulator {regulator_protrend_id}-{regulator_locus_tag}-{regulator_uniprot_accession}'
        return motif.format('transfac')
