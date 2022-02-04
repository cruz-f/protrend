from abc import abstractmethod
from typing import Union, List

from django.db.models import Model
from django.shortcuts import render
from django_neomodel import DjangoNode
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.settings import api_settings

import domain.database as papi
import interfaces.serializers as serializers
from exceptions import ProtrendException
from router import BaseIndexView
from .permissions import SuperUserOrReadOnly


# --------------------------------------------
# BASE API VIEWS
# --------------------------------------------
class ObjectListCreateMixIn:
    """
    View to list and create ProTReND database objects.
    """
    @abstractmethod
    def get_queryset(self) -> Union[List[DjangoNode], List[Model]]:
        pass

    def get(self: Union['ObjectListCreateMixIn', generics.GenericAPIView], request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self: Union['ObjectListCreateMixIn', generics.GenericAPIView], request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        error = self.perform_create(serializer)
        if error is not None:
            return Response(error.message, status=error.status)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def perform_create(serializer):
        try:
            serializer.save()
            return

        except ProtrendException as error:
            return error

    @staticmethod
    def get_success_headers(data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ObjectRetrieveUpdateDestroy:
    """
    View to retrieve, update and delete ProTReND database objects.
    """

    @abstractmethod
    def get_queryset(self, protrend_id: str) -> Union[DjangoNode, Model]:
        pass

    def get_object(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView], protrend_id: str):
        obj = self.get_queryset(protrend_id)
        if obj is None:
            raise ProtrendException(detail='Object not found',
                                    code='get error',
                                    status=status.HTTP_404_NOT_FOUND)
        return obj

    def get(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView],
            request,
            protrend_id: str,
            *args,
            **kwargs):
        obj = self.get_object(protrend_id)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def put(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView],
            request,
            protrend_id: str,
            *args,
            **kwargs):
        partial = kwargs.pop('partial', False)
        obj = self.get_object(protrend_id)

        serializer = self.get_serializer(obj, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        error = self.perform_update(serializer)
        if error is not None:
            return Response(error.message, status=error.status)

        return Response(serializer.data)

    @staticmethod
    def perform_update(serializer):
        try:
            serializer.save()
            return

        except ProtrendException as error:
            return error

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)

    def delete(self: Union['ObjectRetrieveUpdateDestroy', generics.GenericAPIView],
               request,
               protrend_id: str,
               *args,
               **kwargs):
        obj = self.get_object(protrend_id)
        serializer = self.get_serializer(obj)
        error = self.perform_destroy(serializer, obj)
        if error is not None:
            return Response(error.message, status=error.status)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def perform_destroy(serializer, obj):
        try:
            serializer.delete(obj)
            return

        except ProtrendException as error:
            return error


# --------------------------------------------
# CONCRETE API VIEWS
# --------------------------------------------
class IndexView(BaseIndexView):
    """
    ProTReND database REST API. ProTReND provides open programmatic access to the Transcriptional Regulatory Network (TRN) database through a RESTful web API.

    ProTReND's REST API allows users to retrieve structured regulatory data. In addition, the web interface provides a simple yet powerful resource to visualize ProTReND.
    All data can be visualized by navigating through the several biological entities available at the API Index.

    IMPORTANT: USERS PERFORMING MORE THAN 1 REQUEST PER SECOND WILL BE BANNED!
    Please follow the best practices mentioned in the documentation.

    The web API navigation provides detailed visualizations for each biological entity contained in the database.
    """


def best_practices(request):
    return render(request, 'api/best-practices.html')


class EffectorList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here the current list of all effectors in ProTReND.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_effectors()


class EffectorDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Effectors available at ProTReND. Consult here all information available over this effector.

    Effectors can be defined as the biochemical elements that either bind to a given regulator or influence the regulator activity. These biological phenomena can alter the regulator afinity to Transcription Factor Binding Sites (TFBS) and thus changing the regulatory interaction between the regulator and target genes.
    Most effectors can bind to a given regulator which ends up blocking transcription sites.

    Note that, we only provide the effector name and potential associated KEGG compounds. We are working on improving the information provided for each effector.
    """
    serializer_class = serializers.EffectorDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_effector_by_id(protrend_id)


class EvidenceList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here the current list of all evidences in ProTReND.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_evidences()


class EvidenceDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Evidences available at ProTReND. Consult here all information available over this evidence.

    Evidences can be thought of as the experimental techniques and procedures that have lead to the discovery of the regulatory interactions listed in ProTReND.

    We are working on improving the descriptions of all evidences list in ProTReND.
    """
    serializer_class = serializers.EvidenceDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_evidence_by_id(protrend_id)


class GeneList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Genes available at ProTReND. Consult here the current list of all genes in ProTReND.

    Genes are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. In this case, most genes listed in ProTReND are implicity target genes for a set of regulators.
    In detail, ProTReND genes are involved in regulatory interactions. The expression of these genes can be mediated by one or more regulators available at ProTReND.

    Several details are available for each gene including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most genes are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers
    """
    serializer_class = serializers.GeneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_genes()


class GeneDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Genes available at ProTReND. Consult here all information available over this gene.

    Genes are composed by a sequence of nucleotides in DNA that encodes a given RNA or protein. In this case, most genes listed in ProTReND are implicity target genes for a set of regulators.
    In detail, ProTReND genes are involved in regulatory interactions. The expression of these genes can be mediated by one or more regulators available at ProTReND.

    Several details are available for each gene including for instance locus tag, name, synonyms, and function. The corresponding protein sequence and genomic coordinates can also be consulted in the REST API.
    Most genes are referenced to widely known databases, such as UniProt, NCBI protein and NCBI gene, by the corresponding identifiers
    """
    serializer_class = serializers.GeneDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_gene_by_id(protrend_id)


class OperonList(ObjectListCreateMixIn, generics.GenericAPIView):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_operons()


class OperonDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_operon_by_id(protrend_id)


class OrganismList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here the current list of all organisms in ProTReND.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_organisms()


class OrganismDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Organisms available at ProTReND. Consult here all information available over this organism.

    Organisms are listed in ProTReND by their scientific name and NCBI taxonomy identifier.

    Several details are available for each organism including the strain, the NCBI taxonomy identifier, GenBank, RefSeq and Assembly accessions for the reference genome associated with this organism.

    Note that the list of organisms available at ProTReND might contain redundant species due to the ambiguous scientific name found in the collected data sources and NCBI taxonomy misannotations.
    """
    serializer_class = serializers.OrganismDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_organism_by_id(protrend_id)


class PathwayList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Pathways available at ProTReND. Consult here the current list of all pathways in ProTReND.

    A metabolic pathway consists of a set of biochemical reactions occurring within a cellular organism.
    At ProTReND, we provide the name of the metabolic pathways associated with regulators and genes.
    In addition, potential KEGG Pathway identifiers are also provided for each pathway listed here.

    Note that, we only provide the pathway name and potential associated KEGG Pathways. We are working on improving the information provided for each pathway.
    """
    serializer_class = serializers.PathwaySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_pathways()


class PathwayDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Pathways available at ProTReND. Consult here all information available over this pathway.

    A metabolic pathway consists of a set of biochemical reactions occurring within a cellular organism.
    At ProTReND, we provide the name of the metabolic pathways associated with regulators and genes.
    In addition, potential KEGG Pathway identifiers are also provided for each pathway listed here.

    Note that, we only provide the pathway name and potential associated KEGG Pathways. We are working on improving the information provided for each pathway.
    """
    serializer_class = serializers.PathwayDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_pathway_by_id(protrend_id)


class PublicationList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here the current list of all publications in ProTReND.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_publications()


class PublicationDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Publications available at ProTReND. Consult here all information available over this publication.

    A publication consists of a manuscript published in a scientific jornal, a chapter of a scientific book, among others. Most ublications are associated to regulators, genes, and regulatory interactions, and thus supporting regulatory phenomena with exeperimental evidences.

    Note that, we only provide the main details of each publication. The publication can then be consulted using the DOI or PMID.
    """
    serializer_class = serializers.PublicationDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_publication_by_id(protrend_id)


class RegulatorList(ObjectListCreateMixIn, generics.GenericAPIView):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_regulators()


class RegulatorDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_regulator_by_id(protrend_id)


class RegulatoryFamilyList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here the current list of all rfams in ProTReND.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_rfams()


class RegulatoryFamilyDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the Regulatory Families available at ProTReND. Consult here all information available over this rfam.

    A regulatory family comprehends a set of regulators that either share homology among each other, or similar regulatory mechanisms, or common regulatory structures.
    Most regulators are linked to a common regulatory family according to the collected data sources.

    Note that, we only provide the rfam name and sometimes the rfam identifiers. We are working on improving the information provided for each regulatory family.
    """
    serializer_class = serializers.RegulatoryFamilyDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_rfam_by_id(protrend_id)


class RegulatoryInteractionList(ObjectListCreateMixIn, generics.GenericAPIView):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_interactions()


class RegulatoryInteractionDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_interaction_by_id(protrend_id)


class TFBSList(ObjectListCreateMixIn, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the TFBSs available at ProTReND. Consult here the current list of all binding sites in ProTReND.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self):
        return papi.get_binding_sites()


class TFBSDetail(ObjectRetrieveUpdateDestroy, generics.GenericAPIView):
    """
    ProTReND database REST API.

    Open programmatic access for the TFBSs available at ProTReND. Consult here all information available over this binding site.

    Regulators can often bind to specific DNA sequences, which are regularly called cis-elements or Transcription Factor Binding Sites (TFBS) to exert the control of gene expression.
    These binding sites in the organism DNA sequence can be characterized by the nucleotide sequence and genomic coordinates.

    Note that, a binding site might not be regulator-specific. Although these events are extremely rare, more than one regulator can bind to the same cis-element.
    """
    serializer_class = serializers.TFBSDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, SuperUserOrReadOnly]

    def get_queryset(self, protrend_id: str):
        return papi.get_binding_site_by_id(protrend_id)
