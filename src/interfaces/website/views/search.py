from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from interfaces.website.forms import SearchForm
from search.query import query_index


@csrf_protect
def search(request):
    """
    Search for a gene or regulator.
    """
    if request.method == 'POST':
        form = SearchForm(request.POST or None)
        if form.is_valid():
            query = form.cleaned_data['search']
            results = query_index(query)
            results = {key: value.to_dict(orient='records') for key, value in results.items()}

            return render(request, 'website/search.html', {**results, 'query': query, 'form': SearchForm()})

        else:
            return render(request, 'website/search.html', {'form': form})

    else:
        form = SearchForm()

    return render(request, 'website/search.html', {'form': form})
