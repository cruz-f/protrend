from .table import Table


class RegulatorsTable(Table):
    context = 'regulators_table'
    fields = ('protrend_id', 'locus_tag', 'name', 'mechanism', 'detail')
    columns = ('protrend id', 'locus tag', 'name', 'mechanism', 'detail')
    sortable = ('true', 'true', 'true', 'true', 'false')
    types = ('text', 'text', 'text', 'text', 'protrend-regulator-detail-btn')


class RegulatorEffectorsTable(Table):
    context = 'regulator_effectors_table'
    fields = ('protrend_id', 'name')
    columns = ('protrend id', 'name')
    sortable = ('true', 'true')
    types = ('protrend-effector-primary-btn', 'text')


class RegulatorGenesTable(Table):
    context = 'regulator_genes_table'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi')
    sortable = ('true', 'true', 'true', 'true', 'true')
    types = ('protrend-gene-primary-btn', 'text', 'text', 'uniprot-acc-btn', 'ncbi-gene-btn')


class RegulatorBindingsTable(Table):
    context = 'regulator_bindings_table'
    fields = ('protrend_id', 'sequence', 'start', 'stop', 'strand')
    columns = ('protrend id', 'sequence', 'start', 'stop', 'strand')
    sortable = ('true', 'false', 'true', 'true', 'true')
    types = ('protrend-tfbs-primary-btn', 'text', 'text', 'text', 'text')


class RegulatorInteractionsTable(Table):
    context = 'regulator_interactions_table'
    fields = ('protrend_id', 'regulator', 'gene', 'regulatory_effect')
    columns = ('protrend id', 'regulator', 'gene', 'regulatory effect')
    sortable = ('true', 'true', 'true', 'true')
    types = ('protrend-interaction-primary-btn', 'protrend-regulator-black-btn', 'protrend-gene-black-btn',
             'regulatory-effect')
