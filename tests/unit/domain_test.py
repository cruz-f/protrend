import unittest

from django.test import TestCase
from neomodel import clear_neo4j_database, db

from data import *
import domain.dpi as dpi
from ..utils_test_db import populate_db


class DomainTest(TestCase):

    def setUp(self) -> None:
        clear_neo4j_database(db)

    def test_source(self):
        """
        Test the source database.
        """
        obj = dict(name='curation',
                   type='curation')
        obj = dpi.create_objects(Source, (obj,))[0]

        queryset = dpi.get_object(Source, protrend_id='PRT.SRC.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_organism(self):
        """
        Test the organism database.
        """
        obj = dict(name='Escherichia coli str. K-12 substr. MG1655',
                   ncbi_taxonomy=511145)
        obj = dpi.create_objects(Organism, (obj,))[0]

        queryset = dpi.get_object(Organism, protrend_id='PRT.ORG.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_regulator(self):
        """
        Test the regulator database.
        """
        obj = dict(locus_tag='b0001',
                   uniprot_accession='P0AD86',
                   name='thrL',
                   mechanism='transcription factor')
        obj = dpi.create_objects(Regulator, (obj,))[0]

        queryset = dpi.get_object(Regulator, protrend_id='PRT.REG.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_gene(self):
        """
        Test the gene database.
        """
        obj = dict(locus_tag='b0002',
                   uniprot_accession='P00561',
                   name='thrA')
        obj = dpi.create_objects(Gene, (obj,))[0]

        queryset = dpi.get_object(Gene, protrend_id='PRT.GEN.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_tfbs(self):
        """
        Test the tfbs database.
        """
        clear_neo4j_database(db)
        Organism(protrend_id='PRT.ORG.0000001',
                 name='Escherichia coli str. K-12 substr. MG1655',
                 name_factor='escherichia coli str. k-12 substr. mg1655',
                 ncbi_taxonomy=511145).save()

        site_hash = 'PRT.ORG.0000001_AAACCATTTTGCGAT_forward_100100_100115_15'
        obj = dict(site_hash=site_hash,
                   organism='PRT.ORG.0000001',
                   sequence='AAACCATTTTGCGAT',
                   strand='forward',
                   start=100100,
                   stop=100115,
                   length=len('AAACCATTTTGCGAT'))
        obj = dpi.create_objects(TFBS, (obj,))[0]

        queryset = dpi.get_object(TFBS, protrend_id='PRT.TBS.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_effector(self):
        """
        Test the effector database.
        """
        obj = dict(name='Threonine')
        obj = dpi.create_objects(Effector, (obj,))[0]

        queryset = dpi.get_object(Effector, protrend_id='PRT.EFC.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_operon(self):
        """
        Test the operon database.
        """
        clear_neo4j_database(db)
        Gene(protrend_id='PRT.GEN.0000001',
             locus_tag='b0002',
             locus_tag_factor='b0002',
             uniprot_accession='P00561',
             uniprot_accession_factor='p00561',
             name='thrA').save()

        obj = dict(operon_db_id='KO00001',
                   genes=['PRT.GEN.0000001'],
                   name='thr')
        obj = dpi.create_objects(Operon, (obj,))[0]

        queryset = dpi.get_object(Operon, protrend_id='PRT.OPN.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_evidence(self):
        """
        Test the evidence database.
        """
        obj = dict(name='RNA-seq')
        obj = dpi.create_objects(Evidence, (obj,))[0]

        queryset = dpi.get_object(Evidence, protrend_id='PRT.EVI.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_publication(self):
        """
        Test the publication database.
        """
        obj = dict(pmid=100000)
        obj = dpi.create_objects(Publication, (obj,))[0]

        queryset = dpi.get_object(Publication, protrend_id='PRT.PUB.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_interaction(self):
        """
        Test the interaction database.
        """
        clear_neo4j_database(db)
        Organism(protrend_id='PRT.ORG.0000001',
                 name='Escherichia coli str. K-12 substr. MG1655',
                 name_factor='escherichia coli str. k-12 substr. mg1655',
                 ncbi_taxonomy=511145).save()
        Regulator(protrend_id='PRT.REG.0000001',
                  locus_tag='b0001',
                  locus_tag_factor='b0001',
                  uniprot_accession='P0AD86',
                  uniprot_accession_factor='p0ad86',
                  name='thrL',
                  mechanism='transcription factor').save()
        Gene(protrend_id='PRT.GEN.0000001',
             locus_tag='b0002',
             locus_tag_factor='b0002',
             uniprot_accession='P00561',
             uniprot_accession_factor='p00561',
             name='thrA').save()
        site_hash = 'PRT.ORG.0000001_AAACCATTTTGCGAT_forward_100100_100115_15'
        TFBS(protrend_id='PRT.TBS.0000001',
             site_hash=site_hash,
             site_hash_factor=site_hash.lower(),
             organism='PRT.ORG.0000001',
             sequence='AAACCATTTTGCGAT',
             strand='forward',
             start=100100,
             stop=100115,
             length=len('AAACCATTTTGCGAT')).save()
        Effector(protrend_id='PRT.EFC.0000001',
                 name='Threonine',
                 name_factor='threonine').save()

        interaction_hash = 'PRT.ORG.0000001_PRT.REG.0000001_PRT.GEN.0000001_PRT.TBS.0000001_PRT.EFC.0000001_activation'
        obj = dict(interaction_hash=interaction_hash,
                   organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   tfbs='PRT.TBS.0000001',
                   effector='PRT.EFC.0000001',
                   regulatory_effect='activation')
        obj = dpi.create_objects(RegulatoryInteraction, (obj,))[0]

        queryset = dpi.get_object(RegulatoryInteraction, protrend_id='PRT.RIN.0000001')
        object_ = queryset.data[0]
        self.assertEqual(object_.protrend_id, obj.protrend_id)

    def test_relationships(self):
        """
        Test the operon database.
        """
        clear_neo4j_database(db)
        populate_db()

        src_obj = Source.nodes.get(protrend_id='PRT.SRC.0000001')
        organism_obj = Organism.nodes.get(protrend_id='PRT.ORG.0000001')
        regulator_obj = Regulator.nodes.get(protrend_id='PRT.REG.0000001')
        gene_obj = Gene.nodes.get(protrend_id='PRT.GEN.0000001')
        tfbs_obj = TFBS.nodes.get(protrend_id='PRT.TBS.0000001')
        effector_obj = Effector.nodes.get(protrend_id='PRT.EFC.0000001')
        interaction_obj = RegulatoryInteraction.nodes.get(protrend_id='PRT.RIN.0000001')

        evidence_obj = Evidence.nodes.get(protrend_id='PRT.EVI.0000001')
        publication_obj = Publication.nodes.get(protrend_id='PRT.PUB.0000001')

        dpi.create_unique_reverse_relationship(source=src_obj, forward_rel='organism',
                                               backward_rel='data_source', target=organism_obj)
        dpi.create_unique_reverse_relationship(source=src_obj, forward_rel='regulator',
                                               backward_rel='data_source', target=regulator_obj)
        dpi.create_unique_reverse_relationship(source=src_obj, forward_rel='gene',
                                               backward_rel='data_source', target=gene_obj)
        dpi.create_unique_reverse_relationship(source=src_obj, forward_rel='tfbs',
                                               backward_rel='data_source', target=tfbs_obj)
        dpi.create_unique_reverse_relationship(source=src_obj, forward_rel='effector',
                                               backward_rel='data_source', target=effector_obj)
        dpi.create_unique_reverse_relationship(source=src_obj, forward_rel='regulatory_interaction',
                                               backward_rel='data_source', target=interaction_obj)

        self.assertEqual(len(src_obj.organism),
                         len(organism_obj.data_source))
        self.assertEqual(len(src_obj.regulator),
                         len(regulator_obj.data_source))
        self.assertEqual(len(src_obj.gene),
                         len(gene_obj.data_source))
        self.assertEqual(len(src_obj.tfbs),
                         len(tfbs_obj.data_source))
        self.assertEqual(len(src_obj.effector),
                         len(effector_obj.data_source))
        self.assertEqual(len(src_obj.regulatory_interaction),
                         len(interaction_obj.data_source))

        dpi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_organism',
                                               backward_rel='regulatory_interaction', target=organism_obj)
        dpi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_regulator',
                                               backward_rel='regulatory_interaction', target=regulator_obj)
        dpi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_gene',
                                               backward_rel='regulatory_interaction', target=gene_obj)
        dpi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_tfbs',
                                               backward_rel='regulatory_interaction', target=tfbs_obj)
        dpi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_effector',
                                               backward_rel='regulatory_interaction', target=effector_obj)
        dpi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='evidence',
                                               backward_rel='regulatory_interaction', target=evidence_obj)
        dpi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='publication',
                                               backward_rel='regulatory_interaction', target=publication_obj)

        self.assertEqual(len(interaction_obj.data_organism),
                         len(organism_obj.regulatory_interaction))
        self.assertEqual(len(interaction_obj.data_regulator),
                         len(regulator_obj.regulatory_interaction))
        self.assertEqual(len(interaction_obj.data_gene),
                         len(gene_obj.regulatory_interaction))
        self.assertEqual(len(interaction_obj.data_tfbs),
                         len(tfbs_obj.regulatory_interaction))
        self.assertEqual(len(interaction_obj.data_effector),
                         len(effector_obj.regulatory_interaction))
        self.assertEqual(len(interaction_obj.evidence),
                         len(evidence_obj.regulatory_interaction))
        self.assertEqual(len(interaction_obj.publication),
                         len(publication_obj.regulatory_interaction))


if __name__ == '__main__':
    unittest.main()
