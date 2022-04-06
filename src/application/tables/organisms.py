from .table import Table


class OrganismsTable(Table):
    context = 'organisms_table'
    fields = ('protrend_id', 'name', 'ncbi_taxonomy', 'detail')
    columns = ('protrend id', 'name', 'ncbi taxonomy', 'detail')
    sortable = ('true', 'true', 'true', 'false')
    types = ('text', 'text', 'text', 'protrend-organism-detail-btn')


class OrganismRegulatorsTable(Table):
    context = 'organism_regulators_table'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi')
    sortable = ('true', 'true', 'true', 'true', 'true')
    types = ('protrend-regulator-primary-btn', 'text', 'text', 'uniprot-acc-btn', 'ncbi-gene-btn')


class OrganismGenesTable(Table):
    context = 'organism_genes_table'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi')
    sortable = ('true', 'true', 'true', 'true', 'true')
    types = ('protrend-gene-primary-btn', 'text', 'text', 'uniprot-acc-btn', 'ncbi-gene-btn')


class OrganismBindingsTable(Table):
    context = 'organism_bindings_table'
    fields = ('protrend_id', 'sequence', 'start', 'stop', 'strand')
    columns = ('protrend id', 'sequence', 'start', 'stop', 'strand')
    sortable = ('true', 'false', 'true', 'true', 'true')
    types = ('protrend-tfbs-primary-btn', 'text', 'text', 'text', 'text')


class OrganismInteractionsTable(Table):
    context = 'organism_interactions_table'
    fields = ('protrend_id', 'regulator', 'gene', 'regulatory_effect')
    columns = ('protrend id', 'regulator', 'gene', 'regulatory effect')
    sortable = ('true', 'true', 'true', 'true')
    types = ('protrend-interaction-primary-btn', 'protrend-regulator-black-btn', 'protrend-gene-black-btn',
             'regulatory-effect')
