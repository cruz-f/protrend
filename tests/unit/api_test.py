import unittest

from django.test import TestCase

from data import *
from ..utils import clean_db, avoid_throttling


class ApiTest(TestCase):

    def setUp(self) -> None:
        clean_db()

        self.source = Source(protrend_id='PRT.SRC.0000001',
                             name='manual',
                             name_factor='manual',
                             type='curation').save()
        self.organism = Organism(protrend_id='PRT.ORG.0000001',
                                 name='Escherichia coli str. K-12 substr. MG1655',
                                 name_factor='escherichia coli str. k-12 substr. mg1655',
                                 ncbi_taxonomy=511145).save()
        self.regulator = Regulator(protrend_id='PRT.REG.0000001',
                                   locus_tag='b0001',
                                   locus_tag_factor='b0001',
                                   uniprot_accession='P0AD86',
                                   uniprot_accession_factor='p0ad86',
                                   name='thrL',
                                   mechanism='transcription factor').save()
        self.gene = Gene(protrend_id='PRT.GEN.0000001',
                         locus_tag='b0002',
                         locus_tag_factor='b0002',
                         uniprot_accession='P00561',
                         uniprot_accession_factor='p00561',
                         name='thrA').save()
        site_hash = f'{self.organism.protrend_id}_AAACCATTTTGCGAT_forward_100100_100115_15'
        self.tfbs = TFBS(protrend_id='PRT.TBS.0000001',
                         site_hash=site_hash,
                         site_hash_factor=site_hash.lower(),
                         organism=self.organism.protrend_id,
                         sequence='AAACCATTTTGCGAT',
                         strand='forward',
                         start=100100,
                         stop=100115,
                         length=len('AAACCATTTTGCGAT')).save()
        self.effector = Effector(protrend_id='PRT.EFC.0000001',
                                 name='Threonine',
                                 name_factor='threonine').save()
        self.operon = Operon(protrend_id='PRT.OPN.0000001',
                             operon_db_id='KO00001',
                             operon_db_id_factor='ko00001',
                             genes=[self.gene.protrend_id],
                             name='thr').save()
        self.evidence = Evidence(protrend_id='PRT.EVI.0000001',
                                 name='RNA-seq',
                                 name_factor='rna-seq').save()
        self.publication = Publication(protrend_id='PRT.PUB.0000001',
                                       pmid=100000,
                                       pmid_factor='100000').save()

        interaction_hash = f'{self.organism.protrend_id}_{self.regulator.protrend_id}_{self.gene.protrend_id}_' \
                           f'{self.tfbs.protrend_id}_{self.effector.protrend_id}_activation'
        self.interaction = RegulatoryInteraction(protrend_id='PRT.RIN.0000001',
                                                 interaction_hash=interaction_hash,
                                                 interaction_hash_factor=interaction_hash.lower(),
                                                 organism=self.organism.protrend_id,
                                                 regulator=self.regulator.protrend_id,
                                                 gene=self.gene.protrend_id,
                                                 tfbs=self.tfbs.protrend_id,
                                                 effector=self.effector.protrend_id,
                                                 regulatory_effect='activation').save()

    @avoid_throttling
    def test_api_index(self):
        """
        Test if all api end-points are available.
        """
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 14)
        self.assertContains(response, 'interactions')
        self.assertNotContains(response, 'promoters')

    @avoid_throttling
    def test_organism(self):
        """
        Test the organism API.
        """
        response = self.client.get('/api/organisms/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.organism.protrend_id)

    @avoid_throttling
    def test_regulator(self):
        """
        Test the regulator API.
        """
        response = self.client.get('/api/regulators/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.regulator.protrend_id)

    @avoid_throttling
    def test_gene(self):
        """
        Test the gene API.
        """
        response = self.client.get('/api/genes/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.gene.protrend_id)

    @avoid_throttling
    def test_tfbs(self):
        """
        Test the tfbs API.
        """
        response = self.client.get('/api/binding-sites/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.tfbs.protrend_id)

    @avoid_throttling
    def test_effector(self):
        """
        Test the effector API.
        """
        response = self.client.get('/api/effectors/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.effector.protrend_id)

    @avoid_throttling
    def test_operon(self):
        """
        Test the operon API.
        """
        response = self.client.get('/api/operons/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.operon.protrend_id)

    @avoid_throttling
    def test_evidence(self):
        """
        Test the evidence API.
        """
        response = self.client.get('/api/evidences/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.evidence.protrend_id)

    @avoid_throttling
    def test_publication(self):
        """
        Test the publication API.
        """
        response = self.client.get('/api/publications/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.publication.protrend_id)

    @avoid_throttling
    def test_interaction(self):
        """
        Test the operon API.
        """
        response = self.client.get('/api/interactions/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.interaction.protrend_id)

    @avoid_throttling
    def test_trn(self):
        """
        Test the trn API.
        """
        response = self.client.get('/api/trns/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.organism.protrend_id)

    @avoid_throttling
    def test_organism_binding_sites(self):
        """
        Test the organisms-binding-sites API.
        """
        response = self.client.get('/api/organisms-binding-sites/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.organism.protrend_id)

    @avoid_throttling
    def test_regulator_binding_sites(self):
        """
        Test the regulators-binding-sites API.
        """
        response = self.client.get('/api/regulators-binding-sites/')
        status = response.status_code
        data = response.data
        obj = data[0]
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(obj['protrend_id'], self.regulator.protrend_id)


if __name__ == '__main__':
    unittest.main()
