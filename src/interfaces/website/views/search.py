from collections import defaultdict

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from data.models import Gene, Organism, Regulator
from domain import dpi

FILTER_MAP = [
    (Gene,
     ['protrend_id',
      'locus_tag',
      'uniprot_accession',
      'name']),
    (Organism,
     ['protrend_id',
      'name',
      'ncbi_taxonomy']),
    (Regulator,
     ['protrend_id',
      'locus_tag',
      'uniprot_accession',
      'name']),
]


def remove_text_prepositions(query):
    query = query.replace('in', '')
    query = query.replace('of', '')
    query = query.replace('on', '')
    query = query.replace('to', '')
    query = query.replace('from', '')
    query = query.replace('with', '')
    query = query.replace('without', '')
    query = query.replace('for', '')
    query = query.replace('and', '')
    query = query.replace('or', '')
    query = query.replace('not', '')
    query = query.replace('but', '')
    query = query.replace('nor', '')
    query = query.replace('yet', '')
    query = query.replace('so', '')
    query = query.replace('than', '')
    query = query.replace('after', '')
    query = query.replace('before', '')
    query = query.replace('between', '')
    query = query.replace('during', '')
    query = query.replace('since', '')
    query = query.replace('until', '')
    return query


@csrf_protect
def search(request):

    params = request.GET
    if not params:
        return render(request, "website/search.html", {'results': [],
                                                       'query': '',
                                                       'active_page': 'search'})

    if 'q' not in params:
        return render(request, "website/search.html", {'results': [],
                                                       'query': '',
                                                       'active_page': 'search'})

    query = params['q']
    if not query:
        return render(request, "website/search.html", {'results': [],
                                                       'query': '',
                                                       'active_page': 'search'})
    counts = defaultdict(int)
    results = []
    processed_query = remove_text_prepositions(query)
    queries = set([processed_query] + processed_query.split(' '))
    for query_ in queries:
        for filter_ in FILTER_MAP:
            model, fields = filter_
            for field in fields:
                kwargs = {f'{field}__contains': str(query_)}
                objects = dpi.filter_objects(model, fields, **kwargs)
                for object_ in objects:
                    counts[object_.protrend_id] += 1
                    if object_.protrend_id not in results:
                        results.append(object_)

    results = sorted(results, key=lambda k: counts[k.protrend_id], reverse=True)
    return render(request, "website/search.html", {'results': results,
                                                   'query': query,
                                                   'active_page': 'search'})
