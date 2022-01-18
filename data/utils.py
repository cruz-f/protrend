FORWARD = 'FORWARD'
REVERSE = 'REVERSE'
UNKNOWN = 'UNKNOWN'


# noinspection PyPep8Naming
class help_text:
    synonyms = 'A list of synonyms for this gene'
    locus_tag = 'The locus tag for this gene'
    uniprot_accession = 'The UniProt accession for this protein'
    gene_name = 'The name for this gene/protrein'
    function = 'The function for this protein'
    description = 'The description for this protein'
    ncbi_gene = 'The NCBI gene identifier'
    ncbi_protein = 'The NCBI protein identifier'
    genbank_accession = 'The NCBI GenBank accession for this protein'
    refseq_accession = 'The NCBI RefSeq accession for this protein'
    sequence = 'The protein sequence for this protein'
    strand = 'The strand where the gene is located'
    start = 'The start position where the gene is located'
    stop = 'The stop position where the gene is located'


# noinspection PyPep8Naming
class choices:
    strand = {FORWARD: 'forward', REVERSE: 'reverse', UNKNOWN: 'unknown'}


# noinspection PyPep8Naming
class default:
    strand = 'unknown'