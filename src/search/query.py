from pathlib import Path

import pandas as pd
from whoosh import qparser
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.query import FuzzyTerm

from configuration import Configuration
from search.schema import ProtrendSchema


def query_index(query: str, limit: int = None, drop_duplicated: bool = True, n_top_results: int = 50) -> dict:
    """
    Query the index.
    """
    path = Path(Configuration.search_index).joinpath(f'{ProtrendSchema.__name__.lower()}_index')
    ix = open_dir(path)

    og = qparser.OrGroup.factory(0.99)

    parser = MultifieldParser(ix.schema.names(), ix.schema, group=og, termclass=FuzzyTerm)
    parser.remove_plugin_class(qparser.WildcardPlugin)
    parser.add_plugin(qparser.FuzzyTermPlugin())

    parsed_query = parser.parse(query)

    results = []
    with ix.searcher() as searcher:
        for hit in searcher.search(parsed_query, limit=limit):
            result = dict(hit)
            result['score'] = round(hit.score, 4)
            results.append(result)

    df = pd.DataFrame(results)
    df = df.sort_values('score', ascending=False).reset_index(drop=True)

    models = ('organism', 'gene', 'regulator', 'effector', 'pathway', 'regulatory_family')
    tables = {}
    for model in models:
        prefix = f'{model}_'

        table = df.filter(regex=prefix)
        table.columns = table.columns.str.replace(prefix, '')

        if table.empty:
            tables[model] = pd.DataFrame()

        else:
            table = table.assign(score=df['score'])

            if drop_duplicated:
                table = table.drop_duplicates(subset=['protrend_id'])

            table = table.reset_index(drop=True)
            table = table.dropna(subset=['protrend_id'])

            if table.shape[0] > n_top_results:
                table = table.head(n_top_results)

            tables[model] = table

    return tables


if __name__ == '__main__':
    import time
    t0 = time.time()
    res = query_index("lexa escherichi coli")
    print(time.time() - t0)
    # for i in res:
    #     print(i)
