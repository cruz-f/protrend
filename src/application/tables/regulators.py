from .table import Table


class RegulatorsTable(Table):
    context = 'regulators_table'
    fields = ('protrend_id', 'locus_tag', 'name', 'mechanism', 'detail')
    columns = ('protrend id', 'locus tag', 'name', 'mechanism', 'detail')
    sortable = ('true', 'true', 'true', 'true', 'false')
    types = ('text', 'text', 'text', 'text', 'protrend-regulator-detail-btn')
