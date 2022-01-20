from neomodel import ArrayProperty, StringProperty, RelationshipTo

from .base import BaseNode, RequiredNameMixIn
from .relationships import REL_TYPE, SourceRelationship, BaseRelationship
from .utils import help_text


class Pathway(BaseNode, RequiredNameMixIn):
    # properties
    kegg_pathways = ArrayProperty(StringProperty(), help_text=help_text.kegg_pathways)

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, model=SourceRelationship)
    regulator = RelationshipTo('.regulator.Regulator', REL_TYPE, model=BaseRelationship)
    gene = RelationshipTo('.gene.Gene', REL_TYPE, model=BaseRelationship)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'name', 'kegg_pathways',
                  'data_source', 'regulator', 'gene']
