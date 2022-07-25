from pathlib import Path
from typing import Type

from whoosh.fields import SchemaClass
from whoosh.index import create_in, open_dir

from configuration import Configuration
from data.models import Organism, Effector, Pathway, RegulatoryFamily


def create_index(schema_cls: Type[SchemaClass]):
    """
    Create an index using a given schema.
    """
    path = Path(Configuration.search_index)
    if not path.exists():
        path.mkdir(parents=True)

    index_path = path.joinpath(f'{schema_cls.__name__.lower()}_index')
    if not index_path.exists():
        index_path.mkdir(parents=True)

    return create_in(index_path, schema_cls)


def populate_index(schema_cls: Type[SchemaClass]):
    """
    Populate the index with all objects of a given model.
    """
    path = Path(Configuration.search_index).joinpath(f'{schema_cls.__name__.lower()}_index')
    ix = open_dir(path)

    organism_fields = {}
    regulator_fields = {}
    gene_fields = {}
    effector_fields = {}
    pathway_fields = {}
    regulatory_family_fields = {}
    for field in ix.schema.names():

        if field.startswith('organism_'):
            model_field = field.replace('organism_', '')
            organism_fields[field] = model_field

        elif field.startswith('regulator_'):
            model_field = field.replace('regulator_', '')
            regulator_fields[field] = model_field

        elif field.startswith('gene_'):
            model_field = field.replace('gene_', '')
            gene_fields[field] = model_field

        elif field.startswith('effector_'):
            model_field = field.replace('effector_', '')
            effector_fields[field] = model_field

        elif field.startswith('pathway_'):
            model_field = field.replace('pathway_', '')
            pathway_fields[field] = model_field

        elif field.startswith('regulatory_family_'):
            model_field = field.replace('regulatory_family_', '')
            regulatory_family_fields[field] = model_field

    writer = ix.writer()

    for organism in Organism.nodes.all():

        organism_document = {}
        for field, model_field in organism_fields.items():
            organism_document[field] = str(getattr(organism, model_field, None)).encode("utf-8").decode("utf-8")

        writer.add_document(**dict(organism_document))

        for regulator in organism.regulator.all():
            regulator_document = {}

            for field, model_field in regulator_fields.items():
                regulator_document[field] = str(getattr(regulator, model_field, None)).encode("utf-8").decode("utf-8")

            regulator_document.update(dict(organism_document))
            writer.add_document(**dict(regulator_document))

        for gene in organism.gene.all():
            gene_document = {}

            for field, model_field in gene_fields.items():
                gene_document[field] = str(getattr(gene, model_field, None)).encode("utf-8").decode("utf-8")

            gene_document.update(dict(organism_document))
            writer.add_document(**dict(gene_document))

    for effector in Effector.nodes.all():
        effector_document = {}

        for field, model_field in effector_fields.items():
            effector_document[field] = str(getattr(effector, model_field, None)).encode("utf-8").decode("utf-8")

        writer.add_document(**dict(effector_document))

    for pathway in Pathway.nodes.all():
        pathway_document = {}

        for field, model_field in pathway_fields.items():
            pathway_document[field] = str(getattr(pathway, model_field, None)).encode("utf-8").decode("utf-8")

        writer.add_document(**dict(pathway_document))

    for regulatory_family in RegulatoryFamily.nodes.all():
        regulatory_family_document = {}

        for field, model_field in regulatory_family_fields.items():
            regulatory_family_document[field] = str(getattr(regulatory_family, model_field, None)).encode("utf-8").decode("utf-8")

        writer.add_document(**dict(regulatory_family_document))

    writer.commit()


if __name__ == '__main__':
    from search.schema import ProtrendSchema
    from neomodel import db
    db.set_connection(Configuration.bolt_url)

    create_index(ProtrendSchema)
    populate_index(ProtrendSchema)
