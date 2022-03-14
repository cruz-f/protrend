from collections import defaultdict

from application.charts.chart import Chart
from application.charts.colors import Colors
from constants import TRANSCRIPTION_FACTOR, TRANSCRIPTION_ATTENUATOR, TRANSCRIPTION_TERMINATOR, SIGMA_FACTOR, SMALL_RNA


class RegulatorsGenesChart(Chart):
    _chart_type = 'scatter'
    _legend = 'top'
    _title = 'Regulator-Gene Out-Degree Distribution'
    _x_label = 'Regulator-Gene Out-Degree (Kout)'
    _y_label = 'Regulator-Gene Out-Degree Probability P(Kout)'

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


class RegulatorsGenesTopChart(Chart):
    _chart_type = 'bar'
    _orientation = 'vertical'
    _legend = 'top'
    _title = 'Top 25 Regulators by Number of Genes'
    _x_label = 'Gene Frequency'

    @property
    def data(self):
        label = 'Genes'

        labels = sorted(self.objects, key=self.objects.get, reverse=True)[:25]

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('yellow', muted=True),
                     'data': [self.objects[label] for label in labels]}]

        data = {'data': {'labels': labels, 'datasets': datasets}}
        return data


class RegulatoryFamiliesRegulatorsTopChart(Chart):
    _chart_type = 'bar'
    _orientation = 'vertical'
    _legend = 'top'
    _title = 'Top 25 Regulatory Families by Number of Regulators'
    _x_label = 'Regulator Frequency'

    @property
    def data(self):
        label = 'Regulators'

        labels = sorted(self.objects, key=self.objects.get, reverse=True)[:25]

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_color('green', muted=True),
                     'data': [self.objects[label] for label in labels]}]

        data = {'data': {'labels': labels, 'datasets': datasets}}
        return data


class RegulatorsMechanismChart(Chart):
    _chart_type = 'doughnut'
    _legend = 'top'
    _title = 'Distribution of the Regulatory Mechanisms'

    @property
    def data(self):
        labels = {TRANSCRIPTION_FACTOR: 0,
                  TRANSCRIPTION_ATTENUATOR: 0,
                  TRANSCRIPTION_TERMINATOR: 0,
                  SIGMA_FACTOR: 0,
                  SMALL_RNA: 0}

        label = 'Regulators'

        for obj in self.objects:
            if obj.mechanism.lower() in labels:
                labels[obj.mechanism.lower()] += 1

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_palette(len(labels)),
                     'data': list(labels.values())}]

        data = {'data': {'labels': list(labels.keys()), 'datasets': datasets}}
        return data


class RegulatorsExternalChart(Chart):
    _chart_type = 'polarArea'
    _legend = 'right'
    _title = 'NCBI and UniProt External Links'

    @property
    def data(self):
        label = 'Organisms'
        labels = ['UniProtKB', 'NCBI Gene', 'NCBI Protein', 'NCBI RefSeq', 'NCBI GenBank']
        attributes = ('uniprot_accession', 'ncbi_gene', 'ncbi_protein', 'refseq_accession', 'genbank_accession')

        total = len(self.objects)
        freq = defaultdict(int)
        for obj in self.objects:

            for attr in attributes:

                if getattr(obj, attr, None):
                    freq[attr] += 1

        datasets = [{'label': label,
                     'backgroundColor': Colors.get_palette(len(labels), muted=True),
                     'data': [cnt / total for cnt in freq.values()]}]

        data = {'data': {'labels': labels, 'datasets': datasets}}
        return data
