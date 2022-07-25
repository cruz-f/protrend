from whoosh.fields import SchemaClass, TEXT, KEYWORD


class ProtrendSchema(SchemaClass):
    organism_protrend_id = KEYWORD(stored=True, lowercase=True, scorable=True)
    organism_name = KEYWORD(stored=True, lowercase=True, scorable=True)
    organism_ncbi_taxonomy = KEYWORD(stored=True, lowercase=True, scorable=True)
    organism_refseq_accession = KEYWORD(stored=True, lowercase=True, scorable=True)
    organism_genbank_accession = KEYWORD(stored=True, lowercase=True, scorable=True)
    organism_ncbi_assembly = KEYWORD(stored=True, lowercase=True, scorable=True)
    organism_assembly_accession = KEYWORD(stored=True, lowercase=True, scorable=True)

    regulator_protrend_id = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_locus_tag = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_name = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_uniprot_accession = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_synonyms = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_function = TEXT(stored=True)
    regulator_ncbi_gene = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_ncbi_protein = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_genbank_accession = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulator_refseq_accession = KEYWORD(stored=True, lowercase=True, scorable=True)

    gene_protrend_id = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_locus_tag = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_name = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_uniprot_accession = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_synonyms = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_function = TEXT(stored=True)
    gene_ncbi_gene = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_ncbi_protein = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_genbank_accession = KEYWORD(stored=True, lowercase=True, scorable=True)
    gene_refseq_accession = KEYWORD(stored=True, lowercase=True, scorable=True)

    effector_protrend_id = KEYWORD(stored=True, lowercase=True, scorable=True)
    effector_name = KEYWORD(stored=True, lowercase=True, scorable=True)
    effector_kegg_compounds = KEYWORD(stored=True, lowercase=True, scorable=True)

    pathway_protrend_id = KEYWORD(stored=True, lowercase=True, scorable=True)
    pathway_name = KEYWORD(stored=True, lowercase=True, scorable=True)
    pathway_kegg_pathways = KEYWORD(stored=True, lowercase=True, scorable=True)

    regulatory_family_protrend_id = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulatory_family_name = KEYWORD(stored=True, lowercase=True, scorable=True)
    regulatory_family_rfam = KEYWORD(stored=True, lowercase=True, scorable=True)
