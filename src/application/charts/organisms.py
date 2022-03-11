import random
from collections import defaultdict

from .chart import Chart
from .colors import Colors


def _get_species(organism):
    if organism.species:
        return organism.species

    else:
        try:
            species_children = organism.name.split(' ')
            return f'{species_children[0]} {species_children[1]}'

        except IndexError:
            return organism.name


class OrganismsRegulatorsChart(Chart):
    _chart_type = 'scatter'
    _legend = 'top'
    _title = 'Organism-Regulator Out-Degree Distribution'
    _x_label = 'Organism-Regulator Out-Degree (Kout)'
    _y_label = 'Organism-Regulator Out-Degree Probability P(Kout)'

    @property
    def data(self):
        label = 'Out-Degree'

        total = len(self.objects)
        degree_counts = defaultdict(int)
        for value in self.objects.values():
            degree_counts[value] += 1

        degree_coefs = [{'x': degree, 'y': cnt / total} for degree, cnt in degree_counts.items()]

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('red', muted=True),
                     'data': degree_coefs}]
        data = {'data': {'labels': [], 'datasets': datasets}}
        return data


class OrganismsRegulatorsTopChart(Chart):
    _chart_type = 'bar'
    _orientation = 'horizontal'
    _legend = 'right'
    _title = 'Top 10 Organisms by Number of Regulators'
    _x_label = 'Regulator Frequency'
    _y_label = 'Organisms'

    @property
    def data(self):
        label = 'Regulators'

        labels = sorted(self.objects, key=self.objects.get, reverse=True)[:10]

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('yellow', muted=True),
                     'data': [self.objects[label] for label in labels]}]

        data = {'data': {'labels': labels, 'datasets': datasets}}
        return data


class OrganismsTaxaChart(Chart):
    _chart_type = 'bar'
    _orientation = 'horizontal'
    _legend = 'right'
    _title = 'Organisms Taxa'
    _x_label = 'Organism Frequency'
    _y_label = 'Taxonomy Classification'

    @property
    def data(self):
        labels = ['Organisms', 'Species', 'Genera']
        label = 'Organisms'

        genera_counts = set()
        species_counts = set()
        for obj in self.objects:
            species = _get_species(obj)

            species_counts.add(species)

            genera, *_ = species.split(' ')
            genera_counts.add(genera)

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('green', muted=True),
                     'data': [len(self.objects), len(species_counts), len(genera_counts)]}]

        data = {'data': {'labels': labels, 'datasets': datasets}}
        return data


class OrganismsExternalChart(Chart):
    _chart_type = 'polarArea'
    _legend = 'right'
    _title = 'NCBI and UniProt External Links'

    @property
    def data(self):
        label = 'Organisms'
        labels = ['NCBI Taxonomy', 'UniProt Taxonomy', 'NCBI Assembly', 'RefSeq', 'GenBank']
        attributes = ('ncbi_taxonomy', 'uniprot_taxonomy', 'assembly_accession',
                      'refseq_accession', 'genbank_accession')

        total = len(self.objects)
        freq = defaultdict(int)
        for obj in self.objects:

            for attr in attributes:
                if attr == 'uniprot_taxonomy':
                    lookup_attr = 'ncbi_taxonomy'
                else:
                    lookup_attr = attr

                if getattr(obj, lookup_attr, None):
                    freq[attr] += 1

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_palette(len(labels), muted=True),
                     'data': [cnt / total for cnt in freq.values()]}]

        data = {'data': {'labels': labels, 'datasets': datasets}}
        return data


class OrganismTRNChart(Chart):
    _chart_type = 'bar'
    _aspect_ratio = True
    _legend = 'top'
    _title = 'TRN Nodes Distribution'
    _x_label = 'Type of Nodes'
    _y_label = 'Node Frequency'

    @property
    def data(self):
        labels = ['Regulators', 'Genes', 'Binding Sites', 'Interactions']
        label = 'Nodes'

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('blue', muted=True),
                     'data': [len(self.objects.regulator), len(self.objects.gene), len(self.objects.tfbs),
                              len(self.objects.regulatory_interaction)]}]

        data = {'data': {'labels': labels, 'datasets': datasets}}
        return data


class OrganismRegulatorsGenesChart(Chart):
    _chart_type = 'scatter'
    _aspect_ratio = True
    _legend = 'top'
    _title = 'Regulator-Gene Out-Degree Distribution'
    _x_label = 'Regulator Out-Degree (Kout)'
    _y_label = 'Regulator Out-Degree Probability P(Kout)'

    @property
    def data(self):
        label = 'Out-Degree'

        regulators = defaultdict(set)
        for interaction in self.objects.regulatory_interaction:
            regulators[interaction.regulator].add(interaction.gene)

        total = 0
        degree_counts = defaultdict(int)
        for genes in regulators.values():
            degree = len(genes)
            degree_counts[degree] += 1

            total += 1

        degree_coefs = [{'x': degree, 'y': cnt / total} for degree, cnt in degree_counts.items()]

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('red', muted=True),
                     'data': degree_coefs}]
        data = {'data': {'labels': [], 'datasets': datasets}}
        return data


class OrganismGenesRegulatorsChart(Chart):
    _chart_type = 'scatter'
    _aspect_ratio = True
    _legend = 'top'
    _title = 'Gene-Regulator In-Degree Distribution'
    _x_label = 'Genes In-Degree (Kin)'
    _y_label = 'Genes In-Degree Probability P(Kin)'

    @property
    def data(self):
        label = 'In-Degree'

        genes = defaultdict(set)
        for interaction in self.objects.regulatory_interaction:
            genes[interaction.gene].add(interaction.regulator)

        total = 0
        degree_counts = defaultdict(int)
        for regulators in genes.values():
            degree = len(regulators)
            degree_counts[degree] += 1

            total += 1

        degree_coefs = [{'x': degree, 'y': cnt / total} for degree, cnt in degree_counts.items()]

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('green', muted=True),
                     'data': degree_coefs}]
        data = {'data': {'labels': [], 'datasets': datasets}}
        return data


class OrganismRegulatoryEffectChart(Chart):
    _chart_type = 'bar'
    _aspect_ratio = True
    _legend = 'top'
    _title = 'TRN Regulatory Effect Frequency'
    _x_label = 'Type of Regulatory Effect'
    _y_label = 'Regulatory Interaction Frequency'

    @property
    def data(self):
        label = 'Interactions'

        effects = defaultdict(int)
        for interaction in self.objects.regulatory_interaction:
            effects[interaction.regulatory_effect] += 1

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('yellow', muted=True),
                     'data': [cnt for cnt in effects.values()]}]

        data = {'data': {'labels': [label_.title() for label_ in effects.keys()], 'datasets': datasets}}
        return data