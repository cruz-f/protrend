from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from data import Gene, Organism, Regulator
from domain import dpi

FILTER_MAP = [
    (Gene,
     ['locus_tag',
      'uniprot_accession',
      'name']),
    (Organism,
     ['name',
      'ncbi_taxonomy']),
    (Regulator,
     ['locus_tag',
      'uniprot_accession',
      'name']),
]


@csrf_protect
def search(request):
    results = []

    params = request.GET
    if not params:
        return render(request, "website/search.html", {'results': results,
                                                       'query': '',
                                                       'active_page': 'search'})

    if 'q' not in params:
        return render(request, "website/search.html", {'results': results,
                                                       'query': '',
                                                       'active_page': 'search'})

    query = params['q']
    if not query:
        return render(request, "website/search.html", {'results': results,
                                                       'query': '',
                                                       'active_page': 'search'})

    for filter_ in FILTER_MAP:
        model, fields = filter_
        for field in fields:
            kwargs = {f'{field}__contains': str(query)}
            objects = dpi.filter_objects(model, fields, **kwargs)
            results.extend(objects)

    return render(request, "website/search.html", {'results': results,
                                                   'query': query,
                                                   'active_page': 'search'})
