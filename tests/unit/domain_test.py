import unittest

from django.test import TestCase

from data import *
import domain.database as papi
import domain.model_api as mapi
from ..utils import clean_db, populate_db


class ApiTest(TestCase):

    def setUp(self) -> None:
        clean_db()

    def test_source(self):
        """
        Test the source database.
        """
        obj = dict(name='curation',
                   type='curation')
        obj = papi.create_source(**obj)

        source_obj = papi.get_source(protrend_id='PRT.SRC.0000001')
        self.assertEqual(source_obj.protrend_id, obj.protrend_id)

    def test_organism(self):
        """
        Test the organism database.
        """
        obj = dict(name='Escherichia coli str. K-12 substr. MG1655',
                   ncbi_taxonomy=511145)
        obj = papi.create_organism(**obj)

        organism_obj = papi.get_organism(protrend_id='PRT.ORG.0000001')
        self.assertEqual(organism_obj.protrend_id, obj.protrend_id)

    def test_regulator(self):
        """
        Test the regulator database.
        """
        obj = dict(locus_tag='b0001',
                   uniprot_accession='P0AD86',
                   name='thrL',
                   mechanism='transcription factor')
        obj = papi.create_regulator(**obj)

        regulator_obj = papi.get_regulator(protrend_id='PRT.REG.0000001')
        self.assertEqual(regulator_obj.protrend_id, obj.protrend_id)

    def test_gene(self):
        """
        Test the gene database.
        """
        obj = dict(locus_tag='b0002',
                   uniprot_accession='P00561',
                   name='thrA')
        obj = papi.create_gene(**obj)

        gene_obj = papi.get_gene(protrend_id='PRT.GEN.0000001')
        self.assertEqual(gene_obj.protrend_id, obj.protrend_id)

    def test_tfbs(self):
        """
        Test the tfbs database.
        """
        clean_db()
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
        obj = papi.create_binding_site(**obj)

        tfbs_obj = papi.get_binding_site(protrend_id='PRT.TBS.0000001')
        self.assertEqual(tfbs_obj.protrend_id, obj.protrend_id)

    def test_effector(self):
        """
        Test the effector database.
        """
        obj = dict(name='Threonine')
        obj = papi.create_effector(**obj)

        effector_obj = papi.get_effector(protrend_id='PRT.EFC.0000001')
        self.assertEqual(effector_obj.protrend_id, obj.protrend_id)

    def test_operon(self):
        """
        Test the operon database.
        """
        clean_db()
        Gene(protrend_id='PRT.GEN.0000001',
             locus_tag='b0002',
             locus_tag_factor='b0002',
             uniprot_accession='P00561',
             uniprot_accession_factor='p00561',
             name='thrA').save()

        obj = dict(operon_db_id='KO00001',
                   genes=['PRT.GEN.0000001'],
                   name='thr')
        obj = papi.create_operon(**obj)

        operon_obj = papi.get_operon(protrend_id='PRT.OPN.0000001')
        self.assertEqual(operon_obj.protrend_id, obj.protrend_id)

    def test_evidence(self):
        """
        Test the evidence database.
        """
        obj = dict(name='RNA-seq')
        obj = papi.create_evidence(**obj)

        evidence_obj = papi.get_evidence(protrend_id='PRT.EVI.0000001')
        self.assertEqual(evidence_obj.protrend_id, obj.protrend_id)

    def test_publication(self):
        """
        Test the publication database.
        """
        obj = dict(pmid=100000)
        obj = papi.create_publication(**obj)

        pub_obj = papi.get_publication(protrend_id='PRT.PUB.0000001')
        self.assertEqual(pub_obj.protrend_id, obj.protrend_id)

    def test_interaction(self):
        """
        Test the interaction database.
        """
        clean_db()
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
        obj = papi.create_interaction(**obj)

        interaction_obj = papi.get_interaction(protrend_id='PRT.RIN.0000001')
        self.assertEqual(interaction_obj.protrend_id, obj.protrend_id)

    def test_relationships(self):
        """
        Test the operon database.
        """
        clean_db()
        populate_db()

        src_obj = papi.get_source(protrend_id='PRT.SRC.0000001')
        organism_obj = papi.get_organism(protrend_id='PRT.ORG.0000001')
        regulator_obj = papi.get_regulator(protrend_id='PRT.REG.0000001')
        gene_obj = papi.get_gene(protrend_id='PRT.GEN.0000001')
        tfbs_obj = papi.get_binding_site(protrend_id='PRT.TBS.0000001')
        effector_obj = papi.get_effector(protrend_id='PRT.EFC.0000001')
        interaction_obj = papi.get_interaction(protrend_id='PRT.RIN.0000001')

        evidence_obj = Evidence.nodes.get(protrend_id='PRT.EVI.0000001')
        publication_obj = Publication.nodes.get(protrend_id='PRT.PUB.0000001')

        mapi.create_unique_reverse_relationship(source=src_obj, forward_rel='organism',
                                                backward_rel='data_source', target=organism_obj)
        mapi.create_unique_reverse_relationship(source=src_obj, forward_rel='regulator',
                                                backward_rel='data_source', target=regulator_obj)
        mapi.create_unique_reverse_relationship(source=src_obj, forward_rel='gene',
                                                backward_rel='data_source', target=gene_obj)
        mapi.create_unique_reverse_relationship(source=src_obj, forward_rel='tfbs',
                                                backward_rel='data_source', target=tfbs_obj)
        mapi.create_unique_reverse_relationship(source=src_obj, forward_rel='effector',
                                                backward_rel='data_source', target=effector_obj)
        mapi.create_unique_reverse_relationship(source=src_obj, forward_rel='regulatory_interaction',
                                                backward_rel='data_source', target=interaction_obj)

        self.assertEqual(len(mapi.get_related_objects(src_obj, 'organism')),
                         len(mapi.get_related_objects(organism_obj, 'data_source')))
        self.assertEqual(len(mapi.get_related_objects(src_obj, 'regulator')),
                         len(mapi.get_related_objects(regulator_obj, 'data_source')))
        self.assertEqual(len(mapi.get_related_objects(src_obj, 'gene')),
                         len(mapi.get_related_objects(gene_obj, 'data_source')))
        self.assertEqual(len(mapi.get_related_objects(src_obj, 'tfbs')),
                         len(mapi.get_related_objects(tfbs_obj, 'data_source')))
        self.assertEqual(len(mapi.get_related_objects(src_obj, 'effector')),
                         len(mapi.get_related_objects(effector_obj, 'data_source')))
        self.assertEqual(len(mapi.get_related_objects(src_obj, 'regulatory_interaction')),
                         len(mapi.get_related_objects(interaction_obj, 'data_source')))

        mapi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_organism',
                                                backward_rel='regulatory_interaction', target=organism_obj)
        mapi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_regulator',
                                                backward_rel='regulatory_interaction', target=regulator_obj)
        mapi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_gene',
                                                backward_rel='regulatory_interaction', target=gene_obj)
        mapi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_tfbs',
                                                backward_rel='regulatory_interaction', target=tfbs_obj)
        mapi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='data_effector',
                                                backward_rel='regulatory_interaction', target=effector_obj)
        mapi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='evidence',
                                                backward_rel='regulatory_interaction', target=evidence_obj)
        mapi.create_unique_reverse_relationship(source=interaction_obj, forward_rel='publication',
                                                backward_rel='regulatory_interaction', target=publication_obj)

        self.assertEqual(len(mapi.get_related_objects(interaction_obj, 'data_organism')),
                         len(mapi.get_related_objects(organism_obj, 'regulatory_interaction')))
        self.assertEqual(len(mapi.get_related_objects(interaction_obj, 'data_regulator')),
                         len(mapi.get_related_objects(regulator_obj, 'regulatory_interaction')))
        self.assertEqual(len(mapi.get_related_objects(interaction_obj, 'data_gene')),
                         len(mapi.get_related_objects(gene_obj, 'regulatory_interaction')))
        self.assertEqual(len(mapi.get_related_objects(interaction_obj, 'data_tfbs')),
                         len(mapi.get_related_objects(tfbs_obj, 'regulatory_interaction')))
        self.assertEqual(len(mapi.get_related_objects(interaction_obj, 'data_effector')),
                         len(mapi.get_related_objects(effector_obj, 'regulatory_interaction')))
        self.assertEqual(len(mapi.get_related_objects(interaction_obj, 'evidence')),
                         len(mapi.get_related_objects(evidence_obj, 'regulatory_interaction')))
        self.assertEqual(len(mapi.get_related_objects(interaction_obj, 'publication')),
                         len(mapi.get_related_objects(publication_obj, 'regulatory_interaction')))


if __name__ == '__main__':
    unittest.main()
