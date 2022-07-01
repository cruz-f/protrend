from django.http import JsonResponse
from django.urls import reverse

from data import Regulator
from domain import dpi


def regulators_page(request):
    fields = ['protrend_id', 'locus_tag', 'name', 'mechanism']

    regulator_base_url = reverse('regulator', kwargs={'protrend_id': 'regulator_id'})

    limit = int(request.GET.get('limit', 15))
    offset = int(request.GET.get('offset', 0))

    search = request.GET.get('search')
    if search:
        data = {
            'total': 0,
            "totalNotFiltered": 0,
            'rows': []
        }
        for field in fields:
            kwargs = {f'{field}__contains': str(search)}
            query_set = dpi.filter_objects(cls=Regulator, fields=fields, **kwargs)

            for object_ in query_set:
                if object_ not in data['rows']:
                    regulator_url = regulator_base_url.replace('regulator_id', object_.protrend_id)
                    data['rows'].append({
                        'protrend_id': object_.protrend_id,
                        'locus_tag': object_.locus_tag,
                        'name': object_.name,
                        'mechanism': object_.mechanism,
                        'detail': f'<a role="button" class="btn rounded-pill btn-outline-success" href="{regulator_url}"><i class="bi bi-journal-plus pe-2"></i>detail</a>'
                    })

        data['total'] = len(data['rows'])
        data['totalNotFiltered'] = len(data['rows'])

        if data['total'] > limit:
            data['rows'] = data['rows'][offset:offset + limit]
        return JsonResponse(data)

    query_set = dpi.get_objects(cls=Regulator,
                                fields=fields)

    data = {
        'total': query_set.count(),
        "totalNotFiltered": query_set.count(),
        'rows': []
    }

    for object_ in query_set[offset:offset + limit]:
        regulator_url = regulator_base_url.replace('regulator_id', object_.protrend_id)
        data['rows'].append({
            'protrend_id': object_.protrend_id,
            'locus_tag': object_.locus_tag,
            'name': object_.name,
            'mechanism': object_.mechanism,
            'detail': f'<a role="button" class="btn rounded-pill btn-outline-success" href="{regulator_url}"><i class="bi bi-journal-plus pe-2"></i>detail</a>'
        })

    return JsonResponse(data)
