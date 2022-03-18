from django.http import FileResponse

from application.export.fasta import make_fasta_file


def download_fasta(request,
                   identifier: str,
                   locus_tag: str,
                   name: str = None,
                   sequence: str = None,
                   **kwargs):
    if sequence == 'None':
        sequence = None

    description = f'Protein Sequence of {identifier} with locus tag {locus_tag} and name {name}'
    fasta = make_fasta_file(identifier=locus_tag, name=name, sequence=sequence, description=description)
    response = FileResponse(fasta, as_attachment=True, content_type='text/fasta')
    response["content-disposition"] = "attachment; filename=protrend_sequence.fasta"
    return response
