from typing import Union

from django.shortcuts import render

import rest_framework.permissions as drf_permissions
from rest_framework import generics
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework_csv.renderers import CSVRenderer
from drf_renderer_xlsx.renderers import XLSXRenderer

from utils import get_header

import data as data_model

import domain.database as papi
import domain.model_api as mapi

import interfaces.views as views
import interfaces.renderers as renderers
import interfaces.serializers as serializers
import interfaces.permissions as permissions

from router import BaseIndexView


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


class EffectorList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here the current list of all effectors in ProTReND.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return mapi.get_query_set(data_model.Effector)
        return mapi.get_objects(data_model.Effector)


class EffectorDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here all information available over this effector.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Effector, protrend_id=protrend_id)


class EvidenceList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here the current list of all evidences in ProTReND.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return mapi.get_query_set(data_model.Evidence)
        return mapi.get_objects(data_model.Evidence)


class EvidenceDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here all information available over this evidence.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Evidence, protrend_id=protrend_id)


class GeneList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Genes available at ProTReND. Consult here the current list of all genes in ProTReND.

    Genes are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. In this case, most genes listed in ProTReND are implicity target genes for a set of regulators.
    In detail, ProTReND genes are involved in regulatory interactions. The expression of these genes can be mediated by one or more regulators available at ProTReND.

    Several details are available for each gene including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most genes are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers
    """
    serializer_class = serializers.GeneSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_genes_query_set()
        return papi.get_lazy_genes()


class GeneDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
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

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Gene, protrend_id=protrend_id)


class OperonList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Operons available at ProTReND. Consult here the current list of all operons in ProTReND.

    An operon is based on a set of genes which are usually transcribed together as a single unit called a polycistronic unit.

    Several details are available for each operon including the set of genes that compose the operon in ProTReND.
    The corresponding genomic coordinates can also be consulted in the REST API.

    All operons have been retrieved from OperonDB (https://operondb.jp/). Hence, one can consult the OperonDB identifier for each operon listed in ProTReND.
    We advise you to consult OperonDB for more details.
    """
    serializer_class = serializers.OperonSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_operons_query_set()
        return papi.get_lazy_operons()


class OperonDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
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

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Operon, protrend_id=protrend_id)

    def get_renderer_context(self: Union['views.ObjectListMixIn, views.ObjectCreateMixIn', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('genes', )
        header = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context


class OrganismList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here the current list of all organisms in ProTReND.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_organisms_query_set()
        return papi.get_lazy_organisms()


class OrganismDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here all information available over this organism.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Organism, protrend_id=protrend_id)


class PathwayList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Pathways available at ProTReND. Consult here the current list of all pathways in ProTReND.

    A metabolic pathway consists of a set of biochemical reactions occurring within a cellular organism.
    At ProTReND, we provide the name of the metabolic pathways associated with regulators and genes.
    In addition, potential KEGG Pathway identifiers are also provided for each pathway listed here.

    Note that, we only provide the pathway name and potential associated KEGG Pathways. We are working on improving the information provided for each pathway.
    """
    serializer_class = serializers.PathwaySerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return mapi.get_query_set(data_model.Pathway)
        return mapi.get_objects(data_model.Pathway)


class PathwayDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
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

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Pathway, protrend_id=protrend_id)


class PublicationList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here the current list of all publications in ProTReND.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_publications_query_set()
        return papi.get_lazy_publications()


class PublicationDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here all information available over this publication.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Publication, protrend_id=protrend_id)


class RegulatorList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulators available at ProTReND. Consult here the current list of all regulators in ProTReND.

    A regulator consists of a Transcription Factor, Sigma Factor, small RNA (sRNA), Transcription attenuator, or Transcription Terminator. In detail, a regulator can be considered a regulatory protein or RNA regulatory element that mediates the control of gene expression.
    Target genes can be activated or repressed by the binding (or not) of these regulatory elements.

    Regulators are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. Several details are available for each regulator including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most regulators are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers.
    Finally, the mechanism of control of the gene expression is available for each regulator.
    """
    serializer_class = serializers.RegulatorSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_regulators_query_set()
        return papi.get_lazy_regulators()


class RegulatorDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
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

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.Regulator, protrend_id=protrend_id)


class RegulatoryFamilyList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here the current list of all rfams in ProTReND.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilySerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return mapi.get_query_set(data_model.RegulatoryFamily)
        return mapi.get_objects(data_model.RegulatoryFamily)


class RegulatoryFamilyDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here all information available over this rfam.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilyDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.RegulatoryFamily, protrend_id=protrend_id)


class InteractionsList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
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
    serializer_class = serializers.RegulatoryInteractionSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_interactions_query_set()
        return papi.get_lazy_interactions()


class InteractionDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
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

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.RegulatoryInteraction, protrend_id=protrend_id)

    def get_renderer_context(self: Union['views.ObjectListMixIn, views.ObjectCreateMixIn', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('organism', 'regulator', 'gene', 'tfbs', 'effector')
        header = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context


class BindingSitesList(views.ObjectListMixIn, views.ObjectCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites available at ProTReND. Consult here the current list of all binding sites in ProTReND.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_binding_sites_query_set()
        return papi.get_lazy_binding_sites()


class BindingSiteDetail(views.ObjectRetrieveMixIn, views.ObjectUpdateDestroyMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites available at ProTReND. Consult here all information available over this binding site.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSDetailSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly, permissions.SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return mapi.get_object(data_model.TFBS, protrend_id=protrend_id)

    def get_renderer_context(self: Union['views.ObjectListMixIn, views.ObjectCreateMixIn', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('organism',)
        header = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context


class TRNs(views.ObjectListMixIn, generics.GenericAPIView):
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
    serializer_class = serializers.TRNsSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_organisms_query_set()
        return mapi.get_identifiers(data_model.Organism)


class TRN(views.ObjectListMixIn, generics.GenericAPIView):
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
    serializer_class = serializers.TRNSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        organism_id = self.kwargs.get('protrend_id', self.request.query_params.get('protrend_id', None))
        return mapi.filter_objects(data_model.RegulatoryInteraction, organism__exact=organism_id)

    def get_renderer_context(self: Union['views.ObjectListMixIn, views.ObjectCreateMixIn', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('regulator', 'gene', 'tfbs', 'effector')
        header = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context


class OrganismsBindingSites(views.ObjectListMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the current list of all Binding Sites datasets grouped by organism.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The TFBS Dataset API allows one to retrieve all TFBSs associated with a single organism in several standard formats,
    such as FASTA.
    """
    serializer_class = serializers.OrganismsBindingSitesSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_organisms_query_set()
        return mapi.get_identifiers(data_model.Organism)


class OrganismBindingSites(views.ObjectListMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the Binding Site dataset for the selected organism.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The TFBS Dataset API allows one to retrieve all TFBSs associated with a single organism in several standard formats,
    such as FASTA
    """
    serializer_class = serializers.OrganismBindingSitesSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer, renderers.FastaRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        organism_id = self.kwargs.get('protrend_id', self.request.query_params.get('protrend_id', None))
        return mapi.filter_objects(data_model.TFBS, organism__exact=organism_id)


class RegulatorsBindingSites(views.ObjectListMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the current list of all Binding Sites datasets grouped by regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The Regulator-TFBS Dataset API allows one to retrieve all TFBSs associated with a single regulator in several standard formats,
    such as FASTA.
    """
    serializer_class = serializers.RegulatorsBindingSitesSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if views.is_api(self.request):
            return papi.get_lazy_regulators_query_set()
        return mapi.get_identifiers(data_model.Regulator)


class RegulatorBindingSites(views.ObjectListMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Binding Sites datasets available at ProTReND. Consult here the Binding Sites dataset for the selected regulator.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    The Regulator-TFBS Dataset API allows one to retrieve all TFBSs associated with a single regulator in several standard formats,
    such as FASTA
    """
    serializer_class = serializers.RegulatorBindingSitesSerializer
    permission_classes = [drf_permissions.IsAuthenticatedOrReadOnly]
    renderer_classes = (JSONRenderer, CSVRenderer, XLSXRenderer, renderers.FastaRenderer, BrowsableAPIRenderer)

    def get_queryset(self):
        regulator_id = self.kwargs.get('protrend_id', self.request.query_params.get('protrend_id', None))
        interactions = mapi.filter_objects(data_model.RegulatoryInteraction, regulator__exact=regulator_id)

        unique_interactions = {(interaction.regulator, interaction.tfbs): interaction
                               for interaction in interactions
                               if interaction.tfbs}
        return list(unique_interactions.values())

    def get_renderer_context(self: Union['views.ObjectListMixIn', 'views.ObjectCreateMixIn', generics.GenericAPIView]):
        # noinspection PyUnresolvedReferences
        context = super().get_renderer_context()

        serializer_cls = self.get_serializer_class()
        nested_fields = ('regulator', 'tfbs')
        header = get_header(serializer_cls=serializer_cls, nested_fields=nested_fields)

        context['header'] = header
        return context
