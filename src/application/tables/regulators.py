from .table import Table


class RegulatorTable(Table):
    context = 'regulator_table_fields'
    fields = ('protrend_id', 'locus_tag', 'name', 'uniprot_accession', 'ncbi_gene', 'detail')
    columns = ('protrend id', 'locus tag', 'name', 'uniprot', 'ncbi', 'detail')
    sortable = ('true', 'true', 'true', 'true', 'true', 'false')
    types = ('attr', 'attr', 'attr', 'uniprot-btn', 'ncbi-btn', 'regulator-dropdown')
