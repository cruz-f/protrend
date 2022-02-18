import unittest

from django.test import TestCase

from data import *
from ..utils_test_db import clean_db, populate_db


class DataTest(TestCase):

    def setUp(self) -> None:
        clean_db()

    def test_source(self):
        """
        Test the source database.
        """
        obj = Source(protrend_id='PRT.SRC.0000001',
                     name='curation',
                     name_factor='escherichia coli str. k-12 substr. mg1655',
                     type='curation').save()
        self.assertEqual('PRT.SRC.0000001', obj.protrend_id)

    def test_organism(self):
        """
        Test the organism database.
        """
        obj = Organism(protrend_id='PRT.ORG.0000001',
                       name='Escherichia coli str. K-12 substr. MG1655',
                       name_factor='escherichia coli str. k-12 substr. mg1655',
                       ncbi_taxonomy=511145).save()
        self.assertEqual('PRT.ORG.0000001', obj.protrend_id)

    def test_regulator(self):
        """
        Test the regulator database.
        """
        obj = Regulator(protrend_id='PRT.REG.0000001',
                        locus_tag='b0001',
                        locus_tag_factor='b0001',
                        uniprot_accession='P0AD86',
                        uniprot_accession_factor='p0ad86',
                        name='thrL',
                        mechanism='transcription factor').save()
        self.assertEqual('PRT.REG.0000001', obj.protrend_id)

    def test_gene(self):
        """
        Test the gene database.
        """
        obj = Gene(protrend_id='PRT.GEN.0000001',
                   locus_tag='b0002',
                   locus_tag_factor='b0002',
                   uniprot_accession='P00561',
                   uniprot_accession_factor='p00561',
                   name='thrA').save()
        self.assertEqual('PRT.GEN.0000001', obj.protrend_id)

    def test_tfbs(self):
        """
        Test the tfbs database.
        """
        site_hash = 'PRT.ORG.0000001_AAACCATTTTGCGAT_forward_100100_100115_15'
        obj = TFBS(protrend_id='PRT.TBS.0000001',
                   site_hash=site_hash,
                   site_hash_factor=site_hash.lower(),
                   organism='PRT.ORG.0000001',
                   sequence='AAACCATTTTGCGAT',
                   strand='forward',
                   start=100100,
                   stop=100115,
                   length=len('AAACCATTTTGCGAT')).save()
        self.assertEqual('PRT.TBS.0000001', obj.protrend_id)

    def test_effector(self):
        """
        Test the effector database.
        """
        obj = Effector(protrend_id='PRT.EFC.0000001',
                       name='Threonine',
                       name_factor='threonine').save()
        self.assertEqual('PRT.EFC.0000001', obj.protrend_id)

    def test_operon(self):
        """
        Test the operon database.
        """
        obj = Operon(protrend_id='PRT.OPN.0000001',
                     operon_db_id='KO00001',
                     operon_db_id_factor='ko00001',
                     genes=['PRT.GEN.0000001'],
                     name='thr').save()
        self.assertEqual('PRT.OPN.0000001', obj.protrend_id)

    def test_evidence(self):
        """
        Test the evidence database.
        """
        obj = Evidence(protrend_id='PRT.EVI.0000001',
                       name='RNA-seq',
                       name_factor='rna-seq').save()
        self.assertEqual('PRT.EVI.0000001', obj.protrend_id)

    def test_publication(self):
        """
        Test the publication database.
        """
        obj = Publication(protrend_id='PRT.PUB.0000001',
                          pmid=100000,
                          pmid_factor='100000').save()
        self.assertEqual('PRT.PUB.0000001', obj.protrend_id)

    def test_interaction(self):
        """
        Test the interaction database.
        """
        interaction_hash = 'PRT.ORG.0000001_PRT.REG.0000001_PRT.GEN.0000001_PRT.TBS.0000001_PRT.EFC.0000001_activation'
        obj = RegulatoryInteraction(protrend_id='PRT.RIN.0000001',
                                    interaction_hash=interaction_hash,
                                    interaction_hash_factor=interaction_hash.lower(),
                                    organism='PRT.ORG.0000001',
                                    regulator='PRT.REG.0000001',
                                    gene='PRT.GEN.0000001',
                                    tfbs='PRT.TBS.0000001',
                                    effector='PRT.EFC.0000001',
                                    regulatory_effect='activation').save()
        self.assertEqual('PRT.RIN.0000001', obj.protrend_id)

    def test_relationships(self):
        """
        Test the operon database.
        """
        clean_db()

        populate_db()

        _source = Source.nodes.get(protrend_id='PRT.SRC.0000001')

        _interaction = RegulatoryInteraction.nodes.get(protrend_id='PRT.RIN.0000001')
        _interaction.data_source.connect(_source)
        _source.regulatory_interaction.connect(_interaction)

        _organism = Organism.nodes.get(protrend_id='PRT.ORG.0000001')
        _organism.data_source.connect(_source)
        _source.organism.connect(_organism)

        _regulator = Regulator.nodes.get(protrend_id='PRT.REG.0000001')
        _regulator.data_source.connect(_source)
        _source.regulator.connect(_regulator)

        _gene = Gene.nodes.get(protrend_id='PRT.GEN.0000001')
        _gene.data_source.connect(_source)
        _source.gene.connect(_gene)

        _tfbs = TFBS.nodes.get(protrend_id='PRT.TBS.0000001')
        _tfbs.data_source.connect(_source)
        _source.tfbs.connect(_tfbs)

        _effector = Effector.nodes.get(protrend_id='PRT.EFC.0000001')
        _effector.data_source.connect(_source)
        _source.effector.connect(_effector)

        self.assertEqual(len(_source.regulatory_interaction.all()), len(_interaction.data_source.all()))
        self.assertEqual(len(_source.organism.all()), len(_organism.data_source.all()))
        self.assertEqual(len(_source.regulator.all()), len(_regulator.data_source.all()))
        self.assertEqual(len(_source.gene.all()), len(_gene.data_source.all()))
        self.assertEqual(len(_source.tfbs.all()), len(_tfbs.data_source.all()))
        self.assertEqual(len(_source.effector.all()), len(_effector.data_source.all()))

        _evidence = Evidence.nodes.get(protrend_id='PRT.EVI.0000001')

        _publication = Publication.nodes.get(protrend_id='PRT.PUB.0000001')

        _interaction.data_organism.connect(_organism)
        _interaction.data_regulator.connect(_regulator)
        _interaction.data_gene.connect(_gene)
        _interaction.data_tfbs.connect(_tfbs)
        _interaction.data_effector.connect(_effector)
        _interaction.evidence.connect(_evidence)
        _interaction.publication.connect(_publication)

        self.assertGreaterEqual(len(_interaction.data_organism.all()), len(_organism.regulatory_interaction.all()))
        self.assertGreaterEqual(len(_interaction.data_regulator.all()), len(_regulator.regulatory_interaction.all()))
        self.assertGreaterEqual(len(_interaction.data_gene.all()), len(_gene.regulatory_interaction.all()))
        self.assertGreaterEqual(len(_interaction.data_tfbs.all()), len(_tfbs.regulatory_interaction.all()))
        self.assertGreaterEqual(len(_interaction.data_effector.all()), len(_effector.regulatory_interaction.all()))

        _organism.regulatory_interaction.connect(_interaction)
        _organism.regulator.connect(_regulator)
        _organism.gene.connect(_gene)
        _organism.tfbs.connect(_tfbs)

        self.assertEqual(len(_organism.regulatory_interaction.all()), len(_interaction.data_organism.all()))
        self.assertGreaterEqual(len(_organism.regulator.all()), len(_regulator.organism.all()))
        self.assertGreaterEqual(len(_organism.gene.all()), len(_gene.organism.all()))
        self.assertGreaterEqual(len(_organism.tfbs.all()), len(_tfbs.data_organism.all()))

        _regulator.regulatory_interaction.connect(_interaction)
        _regulator.organism.connect(_organism)
        _regulator.gene.connect(_gene)
        _regulator.tfbs.connect(_tfbs)
        _regulator.effector.connect(_effector)

        self.assertEqual(len(_regulator.regulatory_interaction.all()), len(_interaction.data_regulator.all()))
        self.assertEqual(len(_regulator.organism.all()), len(_organism.regulator.all()))
        self.assertGreaterEqual(len(_regulator.gene.all()), len(_gene.regulator.all()))
        self.assertGreaterEqual(len(_regulator.tfbs.all()), len(_tfbs.regulator.all()))
        self.assertGreaterEqual(len(_regulator.effector.all()), len(_effector.regulator.all()))

        _gene.regulatory_interaction.connect(_interaction)
        _gene.organism.connect(_organism)
        _gene.regulator.connect(_regulator)
        _gene.tfbs.connect(_tfbs)

        self.assertEqual(len(_gene.regulatory_interaction.all()), len(_interaction.data_gene.all()))
        self.assertEqual(len(_gene.organism.all()), len(_organism.gene.all()))
        self.assertEqual(len(_gene.regulator.all()), len(_regulator.gene.all()))
        self.assertGreaterEqual(len(_gene.tfbs.all()), len(_tfbs.gene.all()))

        _tfbs.regulatory_interaction.connect(_interaction)
        _tfbs.data_organism.connect(_organism)
        _tfbs.regulator.connect(_regulator)
        _tfbs.gene.connect(_gene)

        self.assertEqual(len(_tfbs.regulatory_interaction.all()), len(_interaction.data_tfbs.all()))
        self.assertEqual(len(_tfbs.data_organism.all()), len(_organism.tfbs.all()))
        self.assertEqual(len(_tfbs.regulator.all()), len(_regulator.tfbs.all()))
        self.assertEqual(len(_tfbs.gene.all()), len(_gene.tfbs.all()))


if __name__ == '__main__':
    unittest.main()
