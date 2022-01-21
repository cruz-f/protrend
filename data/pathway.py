from neomodel import ArrayProperty, StringProperty, RelationshipTo

from .base import BaseNode, NameMixIn
from .relationships import BASE_REL_TYPE, SourceRelationship, BaseRelationship, SOURCE_REL_TYPE
from constants import help_text


class Pathway(BaseNode, NameMixIn):
    # properties
    kegg_pathways = ArrayProperty(StringProperty(), help_text=help_text.kegg_pathways)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, model=SourceRelationship)
    regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', BASE_REL_TYPE, model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'name', 'kegg_pathways',
                  'data_source', 'regulator', 'gene']
