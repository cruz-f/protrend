import functools
import time


def clean_db():
    from data import (Source,
                      Organism,
                      Regulator,
                      Gene,
                      TFBS,
                      Effector,
                      Operon,
                      Evidence,
                      Publication,
                      RegulatoryInteraction)
    nodes = (Source,
             Organism,
             Regulator,
             Gene,
             TFBS,
             Effector,
             Operon,
             Evidence,
             Publication,
             RegulatoryInteraction)
    for node in nodes:
        nodes_instances = node.nodes.all()
        for node_instance in nodes_instances:
            node_instance.delete()


def avoid_throttling(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        time.sleep(0.3)
        return fn(*args, **kwargs)

    return wrapper


def populate_db():
    from data import (Source,
                      Organism,
                      Regulator,
                      Gene,
                      TFBS,
                      Effector,
                      Operon,
                      Evidence,
                      Publication,
                      RegulatoryInteraction)

    Source(protrend_id='PRT.SRC.0000001',
           name='curation',
           name_factor='escherichia coli str. k-12 substr. mg1655',
           type='curation').save()
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
    Operon(protrend_id='PRT.OPN.0000001',
           operon_db_id='KO00001',
           operon_db_id_factor='ko00001',
           genes=['PRT.GEN.0000001'],
           name='thr').save()
    Evidence(protrend_id='PRT.EVI.0000001',
             name='RNA-seq',
             name_factor='rna-seq').save()
    Publication(protrend_id='PRT.PUB.0000001',
                pmid=100000,
                pmid_factor='100000').save()
    interaction_hash = 'PRT.ORG.0000001_PRT.REG.0000001_PRT.GEN.0000001_PRT.TBS.0000001_PRT.EFC.0000001_activation'
    RegulatoryInteraction(protrend_id='PRT.RIN.0000001',
                          interaction_hash=interaction_hash,
                          interaction_hash_factor=interaction_hash.lower(),
                          organism='PRT.ORG.0000001',
                          regulator='PRT.REG.0000001',
                          gene='PRT.GEN.0000001',
                          tfbs='PRT.TBS.0000001',
                          effector='PRT.EFC.0000001',
                          regulatory_effect='activation').save()
