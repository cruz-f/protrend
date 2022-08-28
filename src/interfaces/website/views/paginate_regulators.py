from django.http import JsonResponse
from django.urls import reverse

from data.models import Regulator
from domain import dpi


def regulators_page(request):
    fields = ['protrend_id', 'locus_tag', 'name', 'mechanism']

    regulator_base_url = reverse('regulator', kwargs={'protrend_id': 'regulator_id'})

    limit = int(request.GET.get('limit', 15))
    offset = int(request.GET.get('offset', 0))
    sort = request.GET.get('sort', 'protrend_id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        reversed = True
    else:
        reversed = False

    search = request.GET.get('search')
    if search:
        data = {
            'total': 0,
            "totalNotFiltered": 0,
            'rows': []
        }

        visited_ids = set()

        for field in fields:
            kwargs = {f'{field}__contains': str(search)}
            query_set = dpi.filter_objects(cls=Regulator, fields=fields, **kwargs)

            for object_ in query_set:
                if object_.protrend_id not in visited_ids:
                    regulator_url = regulator_base_url.replace('regulator_id', object_.protrend_id)
                    data['rows'].append({
                        'protrend_id': object_.protrend_id,
                        'locus_tag': object_.locus_tag,
                        'name': object_.name,
                        'mechanism': object_.mechanism,
                        'detail': f'<a role="button" class="btn rounded-pill btn-outline-success" href="{regulator_url}"><i class="bi bi-journal-plus pe-2"></i>detail</a>'
                    })

                visited_ids.add(object_.protrend_id)

        data['total'] = len(data['rows'])
        data['totalNotFiltered'] = len(data['rows'])

        data['rows'] = sorted(data['rows'], reverse=reversed, key=lambda k: k[sort])

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

    data['rows'] = sorted(data['rows'], reverse=reversed, key=lambda k: k[sort])
    return JsonResponse(data)
