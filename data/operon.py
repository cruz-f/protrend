from neomodel import StringProperty, ArrayProperty, RelationshipTo, One

from .base import BaseNode, PositionMixIn
from .relationships import REL_TYPE, SourceRelationship
from .utils import help_text


class Gene(BaseNode, PositionMixIn):
    # base
    entity = 'OPN'

    # properties inherited from PositionMixIn

    # properties
    operon_db_id = StringProperty(required=True, max_length=50, help_text=help_text.operon_db_id)
    name = StringProperty(max_length=50, help_text=help_text.operon_name)
    function = StringProperty(max_length=250, help_text=help_text.operon_function)
    genes = ArrayProperty(StringProperty(), required=True, help_text=help_text.operon_genes)

    # relationships
    data_source = RelationshipTo('.source.Source', REL_TYPE, cardinality=One, model=SourceRelationship)
    evidence = RelationshipTo('.evidence.Evidence', REL_TYPE, cardinality=One)
    publication = RelationshipTo('.publication.Publication', REL_TYPE)
    organism = RelationshipTo('.organism.Organism', REL_TYPE, cardinality=One)
    gene = RelationshipTo('.gene.Gene', REL_TYPE)

    class Meta(BaseNode.Meta):
        fields = ['protrend_id', 'created', 'updated', 'operon_db_id', 'name', 'function', 'genes',
                  'data_source' 'evidence' 'publication' 'organism' 'gene']
