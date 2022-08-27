from rest_framework import renderers

from application.sequences import make_motif, make_jaspar


class JASPARRenderer(renderers.BaseRenderer):
    media_type = 'text/jaspar'
    format = 'jaspar'
    filename = 'protrend_data.jaspar'

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
        return make_jaspar(motif)
