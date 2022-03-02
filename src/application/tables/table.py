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