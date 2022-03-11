class Table:
    context = ''
    fields = ()
    columns = ()
    sortable = ()
    types = ()

    def context_dict(self):
        return {field: {'field': field,
                        'column': col,
                        'sortable': sort,
                        'type': type_}
                for field, col, sort, type_ in zip(self.fields, self.columns, self.sortable, self.types)}
