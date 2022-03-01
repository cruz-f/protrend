class Table:
    context = ''
    fields = ()
    columns = ()
    sortable = ()
    types = ()

    @classmethod
    def context_dict(cls):
        return {field: {'field': field,
                        'column': col,
                        'sortable': sort,
                        'type': type_}
                for field, col, sort, type_ in zip(cls.fields, cls.columns, cls.sortable, cls.types)}


class OrganismTable(Table):
    context = 'organism_table_fields'
    fields = ('protrend_id', 'name', 'ncbi', 'uniprot', 'detail')
    columns = ('protrend id', 'name', 'ncbi', 'uniprot', 'detail')
    sortable = ('true', 'true', 'false', 'false', 'false')
    types = ('attr', 'attr', 'ncbi-dropdown', 'uniprot-dropdown', 'organism-dropdown')


class OrganismRegulatorsTable(Table):
    context = 'organism_regulators_table_fields'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi')
    sortable = ('true', 'true', 'true', 'true', 'true')
    types = ('regulator-btn', 'attr', 'attr', 'uniprot-btn', 'ncbi-btn')


class OrganismGenesTable(Table):
    context = 'organism_genes_table_fields'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi')
    sortable = ('true', 'true', 'true', 'true', 'true')
    types = ('gene-btn', 'attr', 'attr', 'uniprot-btn', 'ncbi-btn')


class OrganismBindingsTable(Table):
    context = 'organism_bindings_table_fields'
    fields = ('protrend_id', 'sequence', 'start', 'stop', 'strand')
    columns = ('protrend id', 'sequence', 'start', 'stop', 'strand')
    sortable = ('true', 'false', 'true', 'true', 'true')
    types = ('binding-btn', 'attr', 'attr', 'attr', 'attr')


class OrganismInteractionsTable(Table):
    context = 'organism_interactions_table_fields'
    fields = ('protrend_id', 'regulator', 'gene', 'regulatory_effect')
    columns = ('protrend id', 'regulator', 'gene', 'regulatory effect')
    sortable = ('true', 'true', 'true', 'true')
    types = ('interaction-btn', 'regulator-btn', 'gene-btn', 'attr')


class RegulatorTable(Table):
    context = 'regulator_table_fields'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene', 'detail')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi', 'detail')
    sortable = ('true', 'true', 'true', 'true', 'true', 'false')
    types = ('attr', 'attr', 'attr', 'uniprot-btn', 'ncbi-btn', 'regulator-dropdown')
