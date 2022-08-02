from neomodel import StringProperty, RelationshipTo, ZeroOrOne, ArrayProperty

from .base import BaseNode
from .relationships import BaseRelationship, BASE_REL_TYPE, SOURCE_REL_TYPE, SourceRelationship, \
    AlignedSequenceRelationship, ALIGNED_SEQUENCE_REL_TYPE
from constants import help_text


class Motif(BaseNode):
    # properties
    locus_tag = StringProperty(required=True, unique_index=True, max_length=100, help_text=help_text.locus_tag)
    locus_tag_factor = StringProperty(required=True, unique_index=True, max_length=100,
                                      help_text=help_text.locus_tag)
    regulator = StringProperty(required=True, max_length=100, help_text=help_text.regulator_id)
    tfbs = ArrayProperty(StringProperty(), help_text=help_text.tfbs_id)
    sequences = ArrayProperty(StringProperty(), help_text=help_text.aligned_sequences)
    consensus_sequence = StringProperty(help_text=help_text.consensus_sequence)

    # relationships
    data_source = RelationshipTo('.source.Source', SOURCE_REL_TYPE, cardinality=ZeroOrOne, model=SourceRelationship)
    organism = RelationshipTo('.organism.Organism', BASE_REL_TYPE, cardinality=ZeroOrOne, model=BaseRelationship)
    data_tfbs = RelationshipTo('.tfbs.TFBS', ALIGNED_SEQUENCE_REL_TYPE, model=AlignedSequenceRelationship)
    data_regulator = RelationshipTo('.regulator.Regulator', BASE_REL_TYPE, cardinality=ZeroOrOne,
                                    model=BaseRelationship)
