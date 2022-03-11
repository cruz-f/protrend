from .table import Table


class OrganismsTable(Table):
    context = 'organism_table_fields'
    fields = ('protrend_id', 'name', 'ncbi', 'uniprot', 'download', 'detail')
    columns = ('protrend id', 'name', 'ncbi', 'uniprot', 'download', 'detail')
    sortable = ('true', 'true', 'false', 'false', 'false', 'false')
    types = ('attr', 'attr', 'ncbi-dropdown', 'uniprot-dropdown', 'organism-download-dropdown', 'organism-dropdown')


class OrganismRegulatorsTable(Table):
    context = 'organism_regulators_table_fields'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi')
    sortable = ('true', 'true', 'true', 'true', 'true')
    types = ('protrend-regulator-btn', 'attr', 'attr', 'uniprot-btn', 'ncbi-gene-btn')


class OrganismGenesTable(Table):
    context = 'organism_genes_table_fields'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi')
    sortable = ('true', 'true', 'true', 'true', 'true')
    types = ('protrend-gene-btn', 'attr', 'attr', 'uniprot-btn', 'ncbi-gene-btn')


class OrganismBindingsTable(Table):
    context = 'organism_bindings_table_fields'
    fields = ('protrend_id', 'sequence', 'start', 'stop', 'strand')
    columns = ('protrend id', 'sequence', 'start', 'stop', 'strand')
    sortable = ('true', 'false', 'true', 'true', 'true')
    types = ('protrend-binding-btn', 'attr', 'attr', 'attr', 'attr')


class OrganismInteractionsTable(Table):
    context = 'organism_interactions_table_fields'
    fields = ('protrend_id', 'regulator', 'gene', 'regulatory_effect')
    columns = ('protrend id', 'regulator', 'gene', 'regulatory effect')
    sortable = ('true', 'true', 'true', 'true')
    types = ('protrend-interaction-btn', 'protrend-regulator-black-btn', 'protrend-gene-black-btn', 'regulatory-effect')
