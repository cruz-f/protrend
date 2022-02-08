import unittest

from django.contrib.auth.models import User
from django.test import TestCase

import domain.model_api as mapi
import domain.database as papi
from interfaces.api.urls import router
from ..utils import clean_db, disable_throttling


class ApiTest(TestCase):

    def setUp(self) -> None:
        clean_db()
        disable_throttling(router)
        test_user = User.objects.get_or_create(username='user_test',
                                               is_superuser=True)[0]
        self.client.force_login(test_user)

    def test_api_index(self):
        """
        Test if all api end-points are available.
        """
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 14)
        self.assertContains(response, 'interactions')
        self.assertNotContains(response, 'promoters')

    def test_organism(self):
        """
        Test the organism API.
        """
        obj = dict(name='Escherichia coli str. K-12 substr. MG1655',
                   ncbi_taxonomy=511145,
                   species='Escherichia coli')
        post = self.client.post('/api/organisms/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = papi.get_organism_by_id('PRT.ORG.0000001')
        self.assertEqual(post.data['protrend_id'], obj.protrend_id)
        self.assertEqual(post.data['name'], obj.name)
        self.assertEqual(post.data['ncbi_taxonomy'], obj.ncbi_taxonomy)

        get = self.client.get('/api/organisms/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

        get_obj = get.data[0]
        self.assertEqual(get_obj['protrend_id'], obj.protrend_id)

        get_detail = self.client.get('/api/organisms/PRT.ORG.0000001/')
        self.assertEqual(get_detail.status_code, 200)

        self.assertEqual(get_detail.data['protrend_id'], obj.protrend_id)
        self.assertEqual(get_detail.data['name'], obj.name)
        self.assertEqual(get_detail.data['ncbi_taxonomy'], obj.ncbi_taxonomy)
        self.assertIsNone(get_detail.data['ncbi_assembly'])

    def test_regulator(self):
        """
        Test the regulator API.
        """
        obj = dict(locus_tag='b0001',
                   uniprot_accession='P0AD86',
                   name='thrL',
                   function='Threonine operon leader',
                   mechanism='transcription factor')
        post = self.client.post('/api/regulators/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = papi.get_regulator_by_id('PRT.REG.0000001')
        self.assertEqual(post.data['protrend_id'], obj.protrend_id)
        self.assertEqual(post.data['locus_tag'], obj.locus_tag)
        self.assertEqual(post.data['uniprot_accession'], obj.uniprot_accession)
        self.assertEqual(post.data['name'], obj.name)
        self.assertEqual(post.data['mechanism'], obj.mechanism)

        get = self.client.get('/api/regulators/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

        get_obj = get.data[0]
        self.assertEqual(get_obj['protrend_id'], obj.protrend_id)

        get_detail = self.client.get('/api/regulators/PRT.REG.0000001/')
        self.assertEqual(get_detail.status_code, 200)

        self.assertEqual(get_detail.data['protrend_id'], obj.protrend_id)
        self.assertEqual(get_detail.data['locus_tag'], obj.locus_tag)
        self.assertEqual(get_detail.data['uniprot_accession'], obj.uniprot_accession)
        self.assertEqual(get_detail.data['name'], obj.name)
        self.assertEqual(get_detail.data['mechanism'], obj.mechanism)
        self.assertIsNone(get_detail.data['ncbi_gene'])

    def test_gene(self):
        """
        Test the gene API.
        """
        obj = dict(locus_tag='b0001',
                   uniprot_accession='P0AD86',
                   name='thrL',
                   function='Threonine operon leader')
        post = self.client.post('/api/genes/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = dict(locus_tag='b0002',
                   uniprot_accession='P00561',
                   name='thrA',
                   function='Threonine kinase')
        post = self.client.post('/api/genes/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = papi.get_gene_by_id('PRT.GEN.0000002')
        self.assertEqual(post.data['protrend_id'], obj.protrend_id)
        self.assertEqual(post.data['locus_tag'], obj.locus_tag)
        self.assertEqual(post.data['uniprot_accession'], obj.uniprot_accession)
        self.assertEqual(post.data['name'], obj.name)

        get = self.client.get('/api/genes/')
        self.assertEqual(get.status_code, 200)
        self.assertGreater(len(get.data), 1)

        get_detail = self.client.get('/api/genes/PRT.GEN.0000002/')
        self.assertEqual(get_detail.status_code, 200)

        self.assertEqual(get_detail.data['protrend_id'], obj.protrend_id)
        self.assertEqual(get_detail.data['locus_tag'], obj.locus_tag)
        self.assertEqual(get_detail.data['uniprot_accession'], obj.uniprot_accession)
        self.assertEqual(get_detail.data['name'], obj.name)
        self.assertIsNone(get_detail.data['ncbi_gene'])

    def test_tfbs(self):
        """
        Test the tfbs API.
        """
        clean_db()
        organism = dict(name='Escherichia coli str. K-12 substr. MG1655',
                        ncbi_taxonomy=511145,
                        species='Escherichia coli')
        organism_post = self.client.post('/api/organisms/', data=organism)
        self.assertEqual(organism_post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   sequence='AAACCATTTTGCGAT',
                   strand='forward',
                   start=100100,
                   stop=100115,
                   length=15)
        post = self.client.post('/api/binding-sites/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = papi.get_binding_site_by_id('PRT.TBS.0000001')
        self.assertEqual(post.data['protrend_id'], obj.protrend_id)
        self.assertEqual(post.data['organism'], organism_post.data['protrend_id'])
        self.assertEqual(post.data['sequence'], obj.sequence)
        self.assertEqual(post.data['strand'], obj.strand)

        get = self.client.get('/api/binding-sites/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

        get_obj = get.data[0]
        self.assertEqual(get_obj['protrend_id'], obj.protrend_id)

        get_detail = self.client.get('/api/binding-sites/PRT.TBS.0000001/')
        self.assertEqual(get_detail.status_code, 200)

        self.assertEqual(get_detail.data['protrend_id'], obj.protrend_id)
        self.assertEqual(get_detail.data['organism']['protrend_id'], organism_post.data['protrend_id'])
        self.assertEqual(get_detail.data['sequence'], obj.sequence)
        self.assertEqual(get_detail.data['strand'], obj.strand)
        self.assertIn(organism_post.data['protrend_id'], str(get_detail.data['data_organism'][0]))

    def test_effector(self):
        """
        Test the effector API.
        """
        obj = dict(name='Threonine')
        post = self.client.post('/api/effectors/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = papi.get_effector_by_id('PRT.EFC.0000001')
        self.assertEqual(post.data['protrend_id'], obj.protrend_id)
        self.assertEqual(post.data['name'], obj.name)

        get = self.client.get('/api/effectors/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

        get_obj = get.data[0]
        self.assertEqual(get_obj['protrend_id'], obj.protrend_id)

        get_detail = self.client.get('/api/effectors/PRT.EFC.0000001/')
        self.assertEqual(get_detail.status_code, 200)

        self.assertEqual(get_detail.data['protrend_id'], obj.protrend_id)
        self.assertEqual(get_detail.data['name'], obj.name)
        self.assertIsNone(get_detail.data['kegg_compounds'])

        patch = self.client.patch('/api/effectors/PRT.EFC.0000001/',
                                  data={'name': 'threonine'},
                                  content_type='application/json')
        self.assertEqual(patch.status_code, 400)
        self.assertEqual(patch.data['code'], 'create or update error')

        patch = self.client.patch('/api/effectors/PRT.EFC.0000001/',
                                  data={'kegg_compounds': ['CO00001']},
                                  content_type='application/json')
        self.assertEqual(patch.status_code, 200)

        get_detail = self.client.get('/api/effectors/PRT.EFC.0000001/')
        self.assertEqual(len(get_detail.data['kegg_compounds']), 1)

        delete = self.client.delete('/api/effectors/PRT.EFC.0000001/')
        self.assertEqual(delete.status_code, 204)

        get = self.client.get('/api/effectors/')
        self.assertEqual(get.status_code, 204)
        self.assertLess(len(get.data[0]), 1)

    def test_interaction(self):
        """
        Test the operon API.
        """
        clean_db()
        organism = dict(name='Escherichia coli str. K-12 substr. MG1655',
                        ncbi_taxonomy=511145,
                        species='Escherichia coli')
        organism_post = self.client.post('/api/organisms/', data=organism)
        self.assertEqual(organism_post.status_code, 201)

        regulator = dict(locus_tag='b0001',
                         uniprot_accession='P0AD86',
                         name='thrL',
                         function='Threonine operon leader',
                         mechanism='transcription factor')
        regulator_post = self.client.post('/api/regulators/', data=regulator)
        self.assertEqual(regulator_post.status_code, 201)

        gene = dict(locus_tag='b0002',
                    uniprot_accession='P00561',
                    name='thrA',
                    function='Threonine kinase')
        gene_post = self.client.post('/api/genes/', data=gene)
        self.assertEqual(gene_post.status_code, 201)

        tfbs = dict(organism='PRT.ORG.0000001',
                    sequence='AAACCATTTTGCGAT',
                    strand='forward',
                    start=100100,
                    stop=100115,
                    length=15)
        tfbs_post = self.client.post('/api/binding-sites/', data=tfbs)
        self.assertEqual(tfbs_post.status_code, 201)

        effector = dict(name='Threonine')
        effector_post = self.client.post('/api/effectors/', data=effector)
        self.assertEqual(effector_post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   regulatory_effect='repression')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   tfbs='PRT.TBS.0000001',
                   regulatory_effect='dual')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   tfbs='PRT.TBS.0000001',
                   effector='PRT.EFC.0000001',
                   regulatory_effect='activation')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = papi.get_interaction_by_id('PRT.RIN.0000003')
        self.assertEqual(post.data['protrend_id'], obj.protrend_id)
        self.assertEqual(post.data['regulatory_effect'], obj.regulatory_effect)
        self.assertEqual(post.data['organism'], organism_post.data['protrend_id'])
        self.assertEqual(post.data['regulator'], regulator_post.data['protrend_id'])
        self.assertEqual(post.data['gene'], gene_post.data['protrend_id'])
        self.assertEqual(post.data['tfbs'], tfbs_post.data['protrend_id'])
        self.assertEqual(post.data['effector'], effector_post.data['protrend_id'])

        get = self.client.get('/api/interactions/')
        self.assertEqual(get.status_code, 200)
        self.assertGreater(len(get.data), 2)

        get_detail = self.client.get('/api/interactions/PRT.RIN.0000003/')
        self.assertEqual(get_detail.status_code, 200)

        obj = papi.get_interaction_by_id('PRT.RIN.0000003')
        self.assertEqual(get_detail.data['protrend_id'], obj.protrend_id)
        self.assertEqual(get_detail.data['regulatory_effect'], obj.regulatory_effect)

        self.assertEqual(get_detail.data['organism']['protrend_id'], organism_post.data['protrend_id'])
        self.assertEqual(get_detail.data['organism']['name'], organism_post.data['name'])

        self.assertEqual(get_detail.data['regulator']['protrend_id'], regulator_post.data['protrend_id'])
        self.assertEqual(get_detail.data['regulator']['locus_tag'], regulator_post.data['locus_tag'])

        self.assertEqual(get_detail.data['gene']['protrend_id'], gene_post.data['protrend_id'])
        self.assertEqual(get_detail.data['gene']['locus_tag'], gene_post.data['locus_tag'])

        self.assertEqual(get_detail.data['tfbs']['protrend_id'], tfbs_post.data['protrend_id'])
        self.assertEqual(get_detail.data['tfbs']['sequence'], tfbs_post.data['sequence'])

        self.assertEqual(get_detail.data['effector']['protrend_id'], effector_post.data['protrend_id'])
        self.assertEqual(get_detail.data['effector']['name'], effector_post.data['name'])

        self.assertIn(organism_post.data['protrend_id'], str(get_detail.data['data_organism'][0]))
        self.assertIn(regulator_post.data['protrend_id'], str(get_detail.data['data_regulator'][0]))
        self.assertIn(gene_post.data['protrend_id'], str(get_detail.data['data_gene'][0]))
        self.assertIn(tfbs_post.data['protrend_id'], str(get_detail.data['data_tfbs'][0]))
        self.assertIn(effector_post.data['protrend_id'], str(get_detail.data['data_effector'][0]))

        organism_get = self.client.get('/api/organisms/PRT.ORG.0000001/')
        regulator_get = self.client.get('/api/regulators/PRT.REG.0000001/')
        gene_get = self.client.get('/api/genes/PRT.GEN.0000001/')

        self.assertIn(organism_get.data['protrend_id'], str(regulator_get.data['organism'][0]))
        self.assertIn(regulator_get.data['protrend_id'], str(organism_get.data['regulator'][0]))
        self.assertIn(regulator_get.data['protrend_id'], str(gene_get.data['regulator'][0]))
        self.assertIn(gene_get.data['protrend_id'], str(regulator_get.data['gene'][0]))

        source = papi.create_source(name='curation', type='curation')
        mapi.create_unique_reverse_relationship(source=source, forward_rel='regulatory_interaction',
                                                backward_rel='data_source', target=obj,
                                                url='https://protrend.bio.di.uminho.pt')

        evidence = dict(name='RNA-seq')
        self.client.post('/api/evidences/', data=evidence)
        evidence = papi.get_evidence_by_id('PRT.EVI.0000001')
        mapi.create_unique_reverse_relationship(source=evidence, forward_rel='regulatory_interaction',
                                                backward_rel='evidence', target=obj)

        publication = dict(pmid=1005053)
        self.client.post('/api/publications/', data=publication)
        publication = papi.get_publication_by_id('PRT.PUB.0000001')
        mapi.create_unique_reverse_relationship(source=publication, forward_rel='regulatory_interaction',
                                                backward_rel='publication', target=obj)

        get_detail = self.client.get('/api/interactions/PRT.RIN.0000003/')
        self.assertEqual(get_detail.status_code, 200)

        self.assertEqual(source.name, get_detail.data['data_source'][0]['name'])
        self.assertEqual('https://protrend.bio.di.uminho.pt', get_detail.data['data_source'][0]['url'])
        self.assertIn(evidence.protrend_id, str(get_detail.data['evidence'][0]))
        self.assertIn(publication.protrend_id, str(get_detail.data['publication'][0]))

        delete = self.client.delete('/api/interactions/PRT.RIN.0000003/')
        self.assertEqual(delete.status_code, 204)

        get = self.client.get('/api/interactions/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 2)

        # TODO: These relationships are maintained as there are more interactions.
        #  But if there are no other interactions, these relationships should be deleted as well.
        organism_get = self.client.get('/api/organisms/PRT.ORG.0000001/')
        regulator_get = self.client.get('/api/regulators/PRT.REG.0000001/')
        gene_get = self.client.get('/api/genes/PRT.GEN.0000001/')

        self.assertIn(organism_get.data['protrend_id'], str(regulator_get.data['organism'][0]))
        self.assertIn(regulator_get.data['protrend_id'], str(organism_get.data['regulator'][0]))
        self.assertIn(regulator_get.data['protrend_id'], str(gene_get.data['regulator'][0]))
        self.assertIn(gene_get.data['protrend_id'], str(regulator_get.data['gene'][0]))

    def test_trn(self):
        """
        Test the trn API.
        """
        clean_db()
        organism = dict(name='Escherichia coli str. K-12 substr. MG1655',
                        ncbi_taxonomy=511145,
                        species='Escherichia coli')
        organism_post = self.client.post('/api/organisms/', data=organism)
        self.assertEqual(organism_post.status_code, 201)

        regulator = dict(locus_tag='b0001',
                         uniprot_accession='P0AD86',
                         name='thrL',
                         function='Threonine operon leader',
                         mechanism='transcription factor')
        regulator_post = self.client.post('/api/regulators/', data=regulator)
        self.assertEqual(regulator_post.status_code, 201)

        gene = dict(locus_tag='b0002',
                    uniprot_accession='P00561',
                    name='thrA',
                    function='Threonine kinase')
        gene_post = self.client.post('/api/genes/', data=gene)
        self.assertEqual(gene_post.status_code, 201)

        tfbs = dict(organism='PRT.ORG.0000001',
                    sequence='AAACCATTTTGCGAT',
                    strand='forward',
                    start=100100,
                    stop=100115,
                    length=15)
        tfbs_post = self.client.post('/api/binding-sites/', data=tfbs)
        self.assertEqual(tfbs_post.status_code, 201)

        effector = dict(name='Threonine')
        effector_post = self.client.post('/api/effectors/', data=effector)
        self.assertEqual(effector_post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   regulatory_effect='repression')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   tfbs='PRT.TBS.0000001',
                   regulatory_effect='dual')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   tfbs='PRT.TBS.0000001',
                   effector='PRT.EFC.0000001',
                   regulatory_effect='activation')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        get = self.client.get('/api/trns/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

        get_detail = self.client.get('/api/trns/PRT.ORG.0000001/')
        self.assertEqual(get_detail.status_code, 200)
        self.assertEqual(len(get_detail.data), 3)

        obj = papi.get_interaction_by_id('PRT.RIN.0000003')

        interaction_3 = None
        for interaction in get_detail.data:
            if interaction['protrend_id'] == 'PRT.RIN.0000003':
                interaction_3 = interaction

        self.assertEqual(interaction_3['protrend_id'], obj.protrend_id)
        self.assertEqual(interaction_3['regulatory_effect'], obj.regulatory_effect)

        self.assertEqual(interaction_3['regulator']['protrend_id'], regulator_post.data['protrend_id'])
        self.assertEqual(interaction_3['regulator']['locus_tag'], regulator_post.data['locus_tag'])

        self.assertEqual(interaction_3['gene']['protrend_id'], gene_post.data['protrend_id'])
        self.assertEqual(interaction_3['gene']['locus_tag'], gene_post.data['locus_tag'])

        self.assertEqual(interaction_3['tfbs']['protrend_id'], tfbs_post.data['protrend_id'])
        self.assertEqual(interaction_3['tfbs']['sequence'], tfbs_post.data['sequence'])

        self.assertEqual(interaction_3['effector']['protrend_id'], effector_post.data['protrend_id'])
        self.assertEqual(interaction_3['effector']['name'], effector_post.data['name'])

    def test_organism_binding_sites(self):
        """
        Test the organisms-binding-sites API.
        """
        clean_db()
        organism = dict(name='Escherichia coli str. K-12 substr. MG1655',
                        ncbi_taxonomy=511145,
                        species='Escherichia coli')
        organism_post = self.client.post('/api/organisms/', data=organism)
        self.assertEqual(organism_post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   sequence='AAACCATTTTGCGAT',
                   strand='forward',
                   start=100100,
                   stop=100115,
                   length=15)
        post = self.client.post('/api/binding-sites/', data=obj)
        self.assertEqual(post.status_code, 201)

        get = self.client.get('/api/organisms-binding-sites/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

        get_detail = self.client.get('/api/organisms-binding-sites/PRT.ORG.0000001/')
        self.assertEqual(get_detail.status_code, 200)
        self.assertEqual(len(get_detail.data), 1)

        obj = papi.get_binding_site_by_id('PRT.TBS.0000001')

        self.assertEqual(get_detail.data[0]['protrend_id'], obj.protrend_id)
        self.assertEqual(get_detail.data[0]['sequence'], obj.sequence)

    def test_regulator_binding_sites(self):
        """
        Test the regulators-binding-sites API.
        """
        clean_db()
        organism = dict(name='Escherichia coli str. K-12 substr. MG1655',
                        ncbi_taxonomy=511145,
                        species='Escherichia coli')
        organism_post = self.client.post('/api/organisms/', data=organism)
        self.assertEqual(organism_post.status_code, 201)

        regulator = dict(locus_tag='b0001',
                         uniprot_accession='P0AD86',
                         name='thrL',
                         function='Threonine operon leader',
                         mechanism='transcription factor')
        regulator_post = self.client.post('/api/regulators/', data=regulator)
        self.assertEqual(regulator_post.status_code, 201)

        gene = dict(locus_tag='b0002',
                    uniprot_accession='P00561',
                    name='thrA',
                    function='Threonine kinase')
        gene_post = self.client.post('/api/genes/', data=gene)
        self.assertEqual(gene_post.status_code, 201)

        tfbs = dict(organism='PRT.ORG.0000001',
                    sequence='AAACCATTTTGCGAT',
                    strand='forward',
                    start=100100,
                    stop=100115,
                    length=15)
        tfbs_post = self.client.post('/api/binding-sites/', data=tfbs)
        self.assertEqual(tfbs_post.status_code, 201)

        effector = dict(name='Threonine')
        effector_post = self.client.post('/api/effectors/', data=effector)
        self.assertEqual(effector_post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   regulatory_effect='repression')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   tfbs='PRT.TBS.0000001',
                   regulatory_effect='dual')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        obj = dict(organism='PRT.ORG.0000001',
                   regulator='PRT.REG.0000001',
                   gene='PRT.GEN.0000001',
                   tfbs='PRT.TBS.0000001',
                   effector='PRT.EFC.0000001',
                   regulatory_effect='activation')
        post = self.client.post('/api/interactions/', data=obj)
        self.assertEqual(post.status_code, 201)

        get = self.client.get('/api/regulators-binding-sites/')
        self.assertEqual(get.status_code, 200)
        self.assertEqual(len(get.data), 1)

        get_detail = self.client.get('/api/regulators-binding-sites/PRT.REG.0000001/')
        self.assertEqual(get_detail.status_code, 200)
        self.assertEqual(len(get_detail.data), 1)

        obj_reg = papi.get_regulator_by_id('PRT.REG.0000001')
        tfbs_reg = papi.get_binding_site_by_id('PRT.TBS.0000001')
        self.assertEqual(get_detail.data[0]['regulator']['protrend_id'], obj_reg.protrend_id)
        self.assertEqual(get_detail.data[0]['regulator']['locus_tag'], obj_reg.locus_tag)
        self.assertEqual(get_detail.data[0]['tfbs']['protrend_id'], tfbs_reg.protrend_id)
        self.assertEqual(get_detail.data[0]['tfbs']['sequence'], tfbs_reg.sequence)


if __name__ == '__main__':
    unittest.main()
