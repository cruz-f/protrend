FORWARD = 'FORWARD'
REVERSE = 'REVERSE'
UNKNOWN = 'UNKNOWN'
TRANSCRIPTION_FACTOR = 'TRANSCRIPTION FACTOR'
TRANSCRIPTION_ATTENUATOR = 'TRANSCRIPTION ATTENUATOR'
TRANSCRIPTION_TERMINATOR = 'TRANSCRIPTION TERMINATOR'
SIGMA_FACTOR = 'SIGMA FACTOR'
SMALL_RNA = 'SMALL RNA (sRNA)'


# noinspection PyPep8Naming
class help_text:
    synonyms = 'A list of synonyms for this gene'
    locus_tag = 'The locus tag for this gene'
    uniprot_accession = 'The UniProt accession for this protein'
    gene_name = 'The name for this gene/protein'
    function = 'The function for this protein'
    description = 'The description for this protein'
    ncbi_gene = 'The NCBI gene identifier'
    ncbi_protein = 'The NCBI protein identifier'
    genbank_accession = 'The NCBI GenBank accession'
    refseq_accession = 'The NCBI RefSeq accession'
    sequence = 'The protein sequence for this protein'
    strand = 'The strand where the gene is located'
    start = 'The start position where the gene is located'
    stop = 'The stop position where the gene is located'
    required_name = 'The name for this item which will be used as main identifier'
    mechanism = 'The regulatory mechanism associated to this regulator'
    organism_name = 'The scientific name for this organism including strain name whenever possible'
    ncbi_taxonomy = 'The NCBI taxonomy identifier'
    species = 'The scientific name for this species'
    strain = 'The strain for this species'
    refseq_ftp = 'The NCBI RefSeq ftp address for this accession'
    genbank_ftp = 'The NCBI GenBank ftp address for this accession'
    ncbi_assembly = 'The NCBI Assembly identifier for the organism genome sequence'
    assembly_accession = 'The NCBI Assembly accession for the organism genome sequence'
    kegg_compounds = 'A list of KEGG compound identifiers associated with this effector'


# noinspection PyPep8Naming
class choices:
    strand = {FORWARD: 'forward', REVERSE: 'reverse', UNKNOWN: 'unknown'}
    mechanism = {TRANSCRIPTION_FACTOR: 'transcription factor', TRANSCRIPTION_ATTENUATOR: 'transcription attenuator',
                 TRANSCRIPTION_TERMINATOR: 'transcription terminator', SIGMA_FACTOR: 'sigma factor',
                 SMALL_RNA: 'small RNA (sRNA)', UNKNOWN: 'unknown'}


# noinspection PyPep8Naming
class default:
    strand = 'unknown'
    mechanism = 'unknown'
