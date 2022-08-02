FORWARD = 'forward'
REVERSE = 'reverse'
UNKNOWN = 'unknown'
TRANSCRIPTION_FACTOR = 'transcription factor'
TRANSCRIPTION_ATTENUATOR = 'transcription attenuator'
TRANSCRIPTION_TERMINATOR = 'transcription terminator'
SIGMA_FACTOR = 'sigma factor'
SMALL_RNA = 'small rna (srna)'
ACTIVATION = 'activation'
REPRESSION = 'repression'
DUAL = 'dual'
LITERATURE = 'literature'
DATABASE = 'database'
CURATION = 'curation'


# noinspection PyPep8Naming
class help_text:
    protrend_id = 'Universal identifier of the ProTReND database'
    created = 'Time tag for the item creation'
    updated = 'Time tag of the item last alteration'

    locus_tag = 'The locus tag for this gene'
    uniprot_accession = 'The UniProt accession for this protein'
    gene_name = 'The name for this gene/protein'
    synonyms = 'A list of synonyms for this gene'
    function = 'The function for this gene/protein'
    description = 'The description for this gene/protein'
    ncbi_gene = 'The NCBI gene identifier'
    ncbi_protein = 'The NCBI protein identifier'
    genbank_accession = 'The NCBI GenBank accession'
    refseq_accession = 'The NCBI RefSeq accession'
    gene_sequence = 'The DNA sequence for this gene'
    protein_sequence = 'The amino acid sequence for this protein'
    strand = 'The strand corresponds to the genomic coordinate forward or reverse'
    start = 'The start corresponds to the genomic coordinate of the item position in the genome sequence'
    stop = 'The stop corresponds to the genomic coordinate of the item position in the genome sequence'
    mechanism = 'The regulatory mechanism associated to this regulator'

    organism_name = 'The scientific name for this organism including strain name whenever possible'
    ncbi_taxonomy = 'The NCBI taxonomy identifier'
    species = 'The scientific name for this species'
    strain = 'The strain for this species'
    refseq_ftp = 'The NCBI RefSeq ftp address for this accession'
    genbank_ftp = 'The NCBI GenBank ftp address for this accession'
    ncbi_assembly = 'The NCBI Assembly identifier for the organism genome sequence'
    assembly_accession = 'The NCBI Assembly accession for the organism genome sequence'

    effector_name = 'The name for this effector'
    kegg_compounds = 'A list of KEGG compound identifiers associated with this effector'

    evidence_name = 'The name for this evidence'
    evidence_description = 'The description for this evidence'

    aligned_sequences = 'The aligned sequences for this motif'
    aligned_sequence = 'The aligned sequence for this motif/TFBS'
    consensus_sequence = 'The consensus sequence for this motif'

    operon_db_id = 'The OperonDB identifier for this operon'
    operon_name = 'The name for this operon'
    operon_function = 'The function for this operon'
    operon_genes = 'The identifiers for the genes associated with this operon'

    pathway_name = 'The name for this pathway'
    kegg_pathways = 'A list of KEGG pathway identifiers associated with this pathway'

    pmid = 'The PubMed identifier for this publication'
    doi = 'The Digital Object Identifier (DOI) for this publication'
    title = 'The title of this publication'
    author = 'The main author of this publication'
    year = 'The year of this publication'

    rfam_name = 'The name for this regulatory family'
    rfam = 'The Regulatory Family (RFAM) name'
    rfam_description = 'The description for this regulatory family'

    organism_id = 'The organism ProTReND identifier'
    regulator_id = 'The regulator ProTReND identifier'
    gene_id = 'The gene ProTReND identifier'
    tfbs_id = 'The TFBS ProTReND identifier'
    effector_id = 'The effector ProTReND identifier'
    regulatory_effect = 'The regulatory effect (e.g. activation, repression, dual and unknown) ' \
                        'of this regulatory interaction'

    source_name = 'The name for this source'
    source_type = 'The type of this data source'
    source_url = 'The web address for this data source'
    source_author = 'The authors of this data source'
    source_description = 'The description for this data source'
    source_external_identifier = 'The external identifier for this data source'

    tfbs_sequence = 'The binding sequence for this TFBS'
    tfbs_length = 'The length of the TFBS sequence'


# noinspection PyPep8Naming
class choices:
    strand = {FORWARD: 'forward', REVERSE: 'reverse', UNKNOWN: 'unknown'}
    mechanism = {TRANSCRIPTION_FACTOR: 'transcription factor', TRANSCRIPTION_ATTENUATOR: 'transcription attenuator',
                 TRANSCRIPTION_TERMINATOR: 'transcription terminator', SIGMA_FACTOR: 'sigma factor',
                 SMALL_RNA: 'small RNA (sRNA)', UNKNOWN: 'unknown'}
    regulatory_effect = {ACTIVATION: 'activation', REPRESSION: 'repression', DUAL: 'dual', UNKNOWN: 'unknown'}
    data_source_type = {LITERATURE: 'literature', DATABASE: 'database', CURATION: 'curation'}


# noinspection PyPep8Naming
class alphabets:
    dna = 'ACTGN.X'
    protrein = 'ACDEFGHIKLMNPQRSTVWYX*.BZJ'
