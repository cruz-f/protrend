from typing import Union

import rest_framework.permissions as drf_permissions
from django.shortcuts import render
from drf_renderer_xlsx.renderers import XLSXRenderer
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_csv.renderers import CSVRenderer

import data as data
import interfaces.permissions as permissions
import interfaces.renderers as renderers
import interfaces.serializers as serializers
import interfaces.views as views
from router import BaseIndexView
from utils import get_header


# --------------------------------------------
# CONCRETE API VIEWS
# --------------------------------------------
class IndexView(BaseIndexView):
    """
    ProTReND database REST API. ProTReND provides open programmatic access to the Transcriptional Regulatory Network (TRN) database through a RESTful web API.

    ProTReND's REST API allows users to retrieve structured regulatory data. In addition, the web interface provides a simple yet powerful resource to visualize ProTReND.
    All data can be visualized by navigating through the several biological entities available at the API Index.

    IMPORTANT:
     - ANONYMOUS USERS PERFORMING MORE THAN 3 REQUESTS PER SECOND WILL BE BANNED!
     - REGISTERED USERS PERFORMING MORE THAN 5 REQUESTS PER SECOND WILL BE BANNED!
    Please follow the best practices mentioned in the documentation.

    The web API navigation provides detailed visualizations for each biological entity contained in the database.
    """
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer)


def best_practices(request):
    return render(request, 'api/best-practices.html')


class EffectorList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here the current list of all effectors in ProTReND.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Effector
    fields = ['protrend_id', 'name', 'kegg_compounds']


class EffectorDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here all information available over this effector.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Effector
    fields = ['protrend_id', 'name', 'kegg_compounds']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}


class EvidenceList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here the current list of all evidences in ProTReND.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Evidence
    fields = ['protrend_id', 'name', 'description']


class EvidenceDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here all information available over this evidence.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Evidence
    fields = ['protrend_id', 'name', 'description']
    targets = {'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {}


class GeneList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Genes available at ProTReND. Consult here the current list of all genes in ProTReND.

    Genes are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. In this case, most genes listed in ProTReND are implicity target genes for a set of regulators.
    In detail, ProTReND genes are involved in regulatory interactions. The expression of these genes can be mediated by one or more regulators available at ProTReND.

    Several details are available for each gene including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most genes are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers
    """
    serializer_class = serializers.GeneListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Gene
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms']


class GeneDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Genes available at ProTReND. Consult here all information available over this gene.

    Genes are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. In this case, most genes listed in ProTReND are implicity target genes for a set of regulators.
    In detail, ProTReND genes are involved in regulatory interactions. The expression of these genes can be mediated by one or more regulators available at ProTReND.

    Several details are available for each gene including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most genes are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers
    """
    serializer_class = serializers.GeneDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Gene
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms',
              'function', 'description', 'ncbi_gene', 'ncbi_protein',
              'genbank_accession', 'refseq_accession', 'sequence', 'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id'],
               'operon': ['protrend_id'],
               'regulator': ['protrend_id'],
               'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}


class OperonList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Operons available at ProTReND. Consult here the current list of all operons in ProTReND.

    An operon is based on a set of genes which are usually transcribed together as a single unit called a polycistronic unit.

    Several details are available for each operon including the set of genes that compose the operon in ProTReND.
    The corresponding genomic coordinates can also be consulted in the REST API.

    All operons have been retrieved from OperonDB (https://operondb.jp/). Hence, one can consult the OperonDB identifier for each operon listed in ProTReND.
    We advise you to consult OperonDB for more details.
    """
    serializer_class = serializers.OperonListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Operon
    fields = ['protrend_id', 'operon_db_id', 'name', 'function', 'genes']


class OperonDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Operons available at ProTReND. Consult here all information available over this operon and its genes.

    An operon is based on a set of genes which are usually transcribed together as a single unit called a polycistronic unit.

    Several details are available for each operon including the set of genes that compose the operon in ProTReND.
    The corresponding genomic coordinates can also be consulted in the REST API.

    All operons have been retrieved from OperonDB (https://operondb.jp/). Hence, one can consult the OperonDB identifier for each operon listed in ProTReND.
    We advise you to consult OperonDB for more details.
    """
    serializer_class = serializers.OperonDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Operon
    fields = ['protrend_id', 'operon_db_id', 'name', 'function', 'genes', 'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id'],
               'gene': ['protrend_id', 'locus_tag', 'uniprot_accession', 'name']}
    relationships = {'data_source': ['url']}

    def get_renderer_context(self: Union['views.APIListView, views.APICreateView', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('genes', )
        header, _ = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context


class OrganismList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here the current list of all organisms in ProTReND.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']


class OrganismDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here all information available over this organism.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain', 'refseq_accession', 'refseq_ftp',
              'genbank_accession', 'genbank_ftp', 'ncbi_assembly', 'assembly_accession']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id'],
               'gene': ['protrend_id'],
               'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}


class PathwayList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Pathways available at ProTReND. Consult here the current list of all pathways in ProTReND.

    A metabolic pathway consists of a set of biochemical reactions occurring within a cellular organism.
    At ProTReND, we provide the name of the metabolic pathways associated with regulators and genes.
    In addition, potential KEGG Pathway identifiers are also provided for each pathway listed here.

    Note that, we only provide the pathway name and potential associated KEGG Pathways. We are working on improving the information provided for each pathway.
    """
    serializer_class = serializers.PathwayListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Pathway
    fields = ['protrend_id', 'name', 'kegg_pathways']


class PathwayDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Pathways available at ProTReND. Consult here all information available over this pathway.

    A metabolic pathway consists of a set of biochemical reactions occurring within a cellular organism.
    At ProTReND, we provide the name of the metabolic pathways associated with regulators and genes.
    In addition, potential KEGG Pathway identifiers are also provided for each pathway listed here.

    Note that, we only provide the pathway name and potential associated KEGG Pathways. We are working on improving the information provided for each pathway.
    """
    serializer_class = serializers.PathwayDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Pathway
    fields = ['protrend_id', 'name', 'kegg_pathways']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id'],
               'gene': ['protrend_id']}
    relationships = {'data_source': ['url']}


class PublicationList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here the current list of all publications in ProTReND.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Publication
    fields = ['protrend_id', 'pmid', 'doi', 'title', 'author', 'year']


class PublicationDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here all information available over this publication.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Publication
    fields = ['protrend_id', 'pmid', 'doi', 'title', 'author', 'year']
    targets = {'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {}


class RegulatorList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulators available at ProTReND. Consult here the current list of all regulators in ProTReND.

    A regulator consists of a Transcription Factor, Sigma Factor, small RNA (sRNA), Transcription attenuator, or Transcription Terminator. In detail, a regulator can be considered a regulatory protein or RNA regulatory element that mediates the control of gene expression.
    Target genes can be activated or repressed by the binding (or not) of these regulatory elements.

    Regulators are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. Several details are available for each regulator including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most regulators are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers.
    Finally, the mechanism of control of the gene expression is available for each regulator.
    """
    serializer_class = serializers.RegulatorListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Regulator
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'mechanism']


class RegulatorDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulators available at ProTReND. Consult here all information available over this regulator.

    A regulator consists of a Transcription Factor, Sigma Factor, small RNA (sRNA), Transcription attenuator, or Transcription Terminator. In detail, a regulator can be considered a regulatory protein or RNA regulatory element that mediates the control of gene expression.
    Target genes can be activated or repressed by the binding (or not) of these regulatory elements.

    Regulators are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. Several details are available for each regulator including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most regulators are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers.
    Finally, the mechanism of control of the gene expression is available for each regulator.
    """
    serializer_class = serializers.RegulatorDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.Regulator
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'synonyms', 'mechanism',
              'function', 'description', 'ncbi_gene',
              'ncbi_protein', 'genbank_accession', 'refseq_accession', 'sequence', 'strand', 'start', 'stop']
    targets = {'data_source': ['name', 'url'],
               'organism': ['protrend_id'],
               'effector': ['protrend_id'],
               'gene': ['protrend_id'],
               'tfbs': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}


class RegulatoryFamilyList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here the current list of all rfams in ProTReND.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilyListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.RegulatoryFamily
    fields = ['protrend_id', 'name', 'mechanism']


class RegulatoryFamilyDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here all information available over this rfam.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilyDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.RegulatoryFamily
    fields = ['protrend_id', 'name', 'mechanism', 'rfam', 'description']
    targets = {'data_source': ['name', 'url'],
               'regulator': ['protrend_id']}
    relationships = {'data_source': ['url']}


class InteractionsList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Interactions available at ProTReND. Consult here the current list of all interactions in ProTReND.

    A regulatory interaction consists of the biological phenomena that involves the control of gene expression by a given regulator. In detail, a regulator activates or represses the expression of its target genes.
    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression. In addition, the regulatory actions promoted by a given regulator can also be influenced by biochemical molecules or metabolites called regulatory effectors.

    In ProTReND, a regulatory interaction comprehends all these regulatory elements:
     - the organism where the regulatory interaction takes place
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.RegulatoryInteractionListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.RegulatoryInteraction
    fields = ['protrend_id', 'organism', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']


class InteractionDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Interactions available at ProTReND. Consult here all information available over this interaction.

    A regulatory interaction consists of the biological phenomena that involves the control of gene expression by a given regulator. In detail, a regulator activates or represses the expression of its target genes.
    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression. In addition, the regulatory actions promoted by a given regulator can also be influenced by biochemical molecules or metabolites called regulatory effectors.

    In ProTReND, a regulatory interaction comprehends all these regulatory elements:
     - the organism where the regulatory interaction takes place
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.RegulatoryInteractionDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.RegulatoryInteraction
    fields = ['protrend_id', 'regulatory_effect']
    targets = {'data_source': ['name', 'url'],
               'evidence': ['protrend_id'],
               'publication': ['protrend_id'],
               'data_organism': ['protrend_id', 'name', 'ncbi_taxonomy'],
               'data_effector': ['protrend_id', 'name'],
               'data_regulator': ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'mechanism'],
               'data_gene': ['protrend_id', 'locus_tag', 'uniprot_accession', 'name'],
               'data_tfbs': ['protrend_id', 'sequence', 'strand', 'start', 'stop',]}
    relationships = {'data_source': ['url']}

    def get_renderer_context(self: Union['views.APIListView, views.APICreateView', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('organism', 'regulator', 'gene', 'tfbs', 'effector')
        header, _ = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context


class BindingSitesList(views.APIListView, views.APICreateView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites available at ProTReND. Consult here the current list of all binding sites in ProTReND.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.TFBS
    fields = ['protrend_id', 'organism', 'sequence', 'strand', 'start', 'stop', 'length']


class BindingSiteDetail(views.APIRetrieveView, views.APIUpdateDestroyView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites available at ProTReND. Consult here all information available over this binding site.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]
    model = data.TFBS
    fields = ['protrend_id', 'organism', 'sequence', 'strand', 'start', 'stop', 'length']
    targets = {'data_source': ['name', 'url'],
               'evidence': ['protrend_id'],
               'publication': ['protrend_id'],
               'data_organism': ['protrend_id', 'name', 'ncbi_taxonomy'],
               'regulator': ['protrend_id'],
               'gene': ['protrend_id'],
               'regulatory_interaction': ['protrend_id']}
    relationships = {'data_source': ['url']}

    def get_renderer_context(self: Union['views.APIListView, views.APICreateView', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('organism', )
        header, _ = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context


class TRNList(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Transcriptional Regulatory Networks (TRNs) available at ProTReND. Consult here the current list of all TRNs in ProTReND.

    TRNs encode instructions for the expression of target genes in response to regulatory proteins.
    TRNs can be thought of as computational modeling tools that allow to describe meaningful regulatory interactions between regulators and target genes.

    In ProTReND, a TRN is organism-specific and comprehends all these regulatory elements:
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.TRNListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Organism
    fields = ['protrend_id']


class TRN(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Transcriptional Regulatory Networks (TRNs) available at ProTReND. Consult here all information available over this TRN.

    TRNs encode instructions for the expression of target genes in response to regulatory proteins.
    TRNs can be thought of as computational modeling tools that allow to describe meaningful regulatory interactions between regulators and target genes.

    In ProTReND, a TRN is organism-specific and comprehends all these regulatory elements:
     - the regulator that mediates the control of gene expression
     - the target gene whose expression is being controlled by the regulatory element
     - the TFBS (might not be available for all interactions) where the regulator binds to activate/repress the target gene
     - the effector which can bind or not to a regulator altering the regulatory action of this element
     - the regulatory effect which consists of the outcome of the interaction between the regulator and the target gene, namely target gene activation, inactivation, dual or unknown behavior
    """
    serializer_class = serializers.TRNDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    targets = {'regulatory_interaction': ['protrend_id', 'regulator', 'gene', 'tfbs', 'effector', 'regulatory_effect']}


class OrganismsBindingSites(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the current list of all Binding Sites datasets grouped by organism.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The TFBS Dataset API allows one to retrieve all TFBSs associated with a single organism in several standard formats, such as FASTA.
    """
    serializer_class = serializers.OrganismBindingSitesListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Organism
    fields = ['protrend_id']


class OrganismBindingSites(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the Binding Site dataset for the selected organism.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The TFBS Dataset API allows one to retrieve all TFBSs associated with a single organism in several standard formats, such as FASTA
    """
    serializer_class = serializers.OrganismBindingSitesDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer, renderers.FastaRenderer, BrowsableAPIRenderer)
    model = data.Organism
    fields = ['protrend_id', 'name', 'ncbi_taxonomy', 'species', 'strain']
    targets = {'tfbs': ['protrend_id', 'sequence', 'strand', 'start', 'stop']}


class RegulatorsBindingSites(views.APIListView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the current list of all Binding Sites datasets grouped by regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The Regulator-TFBS Dataset API allows one to retrieve all TFBSs associated with a single regulator in several standard formats,
    such as FASTA.
    """
    serializer_class = serializers.RegulatorBindingSitesListSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    model = data.Regulator
    fields = ['protrend_id']


class RegulatorBindingSites(views.APIRetrieveView, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the Binding Sites dataset for the selected regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The Regulator-TFBS Dataset API allows one to retrieve all TFBSs associated with a single regulator in several standard formats,
    such as FASTA
    """
    serializer_class = serializers.RegulatorBindingSitesDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer, renderers.FastaRenderer, BrowsableAPIRenderer)
    model = data.Regulator
    fields = ['protrend_id', 'locus_tag', 'uniprot_accession', 'name', 'mechanism']
    targets = {'tfbs': ['protrend_id', 'sequence', 'strand', 'start', 'stop']}

