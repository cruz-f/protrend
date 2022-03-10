from typing import Union, Type, List, Dict

from django_neomodel import DjangoNode

from .utils import raise_exception
from ..neo import NeoNode, NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet
from ..neo.query_set import add_query_sets

_model_type = Union[Type[DjangoNode], Type[NeoNode]]
_model = Union[DjangoNode, NeoNode]


# ---------------------------------------------------------
# GET A QUERY SET
# ---------------------------------------------------------
def get_query_set(cls: _model_type,
                  fields: List[str] = None,
                  target: str = None,
                  target_fields: List[str] = None,
                  relationship_fields: List[str] = None) -> Union[NeoQuerySet,
                                                                  NeoLinkedQuerySet,
                                                                  NeoHyperLinkedQuerySet]:
    if not target:
        return NeoQuerySet(source=cls, fields=fields)

    if not relationship_fields:
        return NeoLinkedQuerySet(source=cls, fields=fields, target=target, target_fields=target_fields)

    return NeoHyperLinkedQuerySet(source=cls, fields=fields, target=target, target_fields=target_fields,
                                  relationship_fields=relationship_fields)


# ---------------------------------------------------------
# Bulk Object Queries
# ---------------------------------------------------------
@raise_exception
def get_objects(cls: _model_type,
                fields: List[str] = None,
                targets: Dict[str, List[str]] = None,
                relationships: Dict[str, List[str]] = None) -> Union[NeoQuerySet,
                                                                     NeoLinkedQuerySet,
                                                                     NeoHyperLinkedQuerySet]:
    """
    It builds a NeoQuerySet that retrieves all nodes from the database based on the model type.
    The model label will be used in the cypher query to the database.

    The list of fields that must be fetched from the database for a given node can be used to speed up the cypher query.
    Fields' list should contain only node properties that must be fetched and loaded into a NeoNode.

    A NeoLinkedQuerySet can be obtained when submitting targets. In this case, the NeoLinkedQuerySet retrieves
    all nodes based on the model type, while collecting all nodes connected to these fetched nodes.
    The connected nodes are retrieved from the database based on the relationship definition in the model type.

    A NeoHyperLinkedQuerySet can be obtained when submitting targets and relationships. In this case,
    the NeoLinkedQuerySet retrieves all nodes from the database based on the model type,
    while collecting both all nodes connected to these fetched nodes and relationships objects.
    The relationships are retrieved from the database based on the relationship definition in the model type.

    Keys in the targets and relationships dictionaries must declare which target/relationship attribute
    defined in the model type should be used to perform a linked or hyperlinked query set and thus fetch the connected
    nodes and relationships.

    Values in the targets and relationships dictionaries will be interpreted as lists of fields
    that must be retrieved from the connected nodes and relationships objects and then loaded into NeoNodes.

    :type cls: Union[Type[DjangoNode], Type[NeoNode]]
    :type fields: List[str]
    :type targets: Dict[str, List[str]]
    :type relationships: Dict[str, List[str]]

    :param cls: A neomodel structured node type available at the data model package
    that represents a node in the Neo4j ProTReND database
    :param fields: A list of fields that will be used to fetch the node properties and load them into a NeoNode instance
    :param targets: A dictionary of target-fields pairs that will be used to fetch the connected nodes' properties
    and load them into NeoNodes instances
    :param relationships: A dictionary of relationship-fields pairs that will be used to fetch
    the connected relationships' properties and load them into NeoNodes instances

    :return: It returns a NeoQuerySet, NeoLinkedQuerySet, or NeoHyperLinkedQuerySet based on the inputs,
    namely targets and relationships
    """
    if not targets:
        targets = {}

    if not relationships:
        relationships = {}

    if not targets and relationships:
        raise ValueError('Cannot fetch relationships without targets')

    query_sets = []
    for target, target_fields in targets.items():
        relationship_fields = relationships.get(target)
        query_set = get_query_set(cls=cls, fields=fields, target=target, target_fields=target_fields,
                                  relationship_fields=relationship_fields)
        query_set.all()
        query_sets.append(query_set)

    if len(query_sets) == 1:
        return query_sets[0]

    query_set = add_query_sets(*query_sets)
    return query_set


@raise_exception
def get_identifiers(cls: _model_type, targets: List[str] = None) -> Union[NeoQuerySet,
                                                                          NeoLinkedQuerySet,
                                                                          NeoHyperLinkedQuerySet]:
    """
    It builds a NeoQuerySet that retrieves all nodes from the database based on the model type.
    The model label will be used in the cypher query to the database.

    In this case, only the protrend identifiers will be retrieved from the database.

    A NeoLinkedQuerySet can be obtained when submitting targets. In this case, the NeoLinkedQuerySet retrieves
    all nodes based on the model type, while collecting all nodes connected to these fetched nodes.
    The connected nodes are retrieved from the database based on the relationship definition in the model type.

    As with the source nodes, the query set will only retrieve protrend identifiers for the targets' nodes

    :type cls: Union[Type[DjangoNode], Type[NeoNode]]
    :type targets: List[str]

    :param cls: A neomodel structured node type available at the data model package
    that represents a node in the Neo4j ProTReND database
    :param targets: A list of targets that will be used to fetch the connected nodes
    and load their protrend identifiers into NeoNodes instances

    :return: It returns a NeoQuerySet, NeoLinkedQuerySet, or NeoHyperLinkedQuerySet based on the inputs,
    namely targets and relationships
    """
    if not targets:
        targets = []

    query_sets = []
    for target in targets:
        query_set = get_query_set(cls=cls,
                                  fields=['protrend_id'],
                                  target=target,
                                  target_fields=['protrend_id'])
        query_set.all()
        query_sets.append(query_set)

    if len(query_sets) == 1:
        return query_sets[0]

    query_set = add_query_sets(*query_sets)
    return query_set


@raise_exception
def count_objects(cls: _model_type, target: str = None) -> Union[int, Dict[str, int]]:
    """
    It builds a NeoQuerySet that retrieves the count of all nodes in the database based on the model type.
    The model label will be used in the cypher query to the database.

    A NeoLinkedQuerySet can be obtained when submitting a target. In this case, the NeoLinkedQuerySet retrieves
    the count of all connected nodes to each matched source node.
    The connected nodes are retrieved from the database based on the relationship definition in the model type.

    :type cls: Union[Type[DjangoNode], Type[NeoNode]]
    :type target: str

    :param cls: A neomodel structured node type available at the data model package
    that represents a node in the Neo4j ProTReND database
    :param target: The target that will be used to fetch the connected nodes and retrieve the connected nodes counts

    :return: It returns the count of all nodes in the database based on the model type,
    or the count of all connected nodes to each matched source node. The latter option yields a dictionary
    of protrend_id-count
    """
    if target:
        query_set = NeoLinkedQuerySet(source=cls, fields=['protrend_id'], target=target, target_fields=['protrend_id'])
    else:
        query_set = NeoQuerySet(source=cls)

    return query_set.count()


@raise_exception
def filter_objects(cls: _model_type,
                   fields: List[str] = None,
                   targets: Dict[str, List[str]] = None,
                   relationships: Dict[str, List[str]] = None,
                   **kwargs) -> Union[NeoQuerySet, NeoLinkedQuerySet, NeoHyperLinkedQuerySet]:
    """
    It builds a NeoQuerySet that filters nodes from the database based on the model type and query filters.
    The model label will be used in the cypher query to the database.

    The list of fields that must be fetched from the database for a given node can be used to speed up the cypher query.
    Fields' list should contain only node properties that must be fetched and loaded into a NeoNode.

    A NeoLinkedQuerySet can be obtained when submitting targets. In this case, the NeoLinkedQuerySet filters
    all nodes based on the model type, while collecting all nodes connected to these fetched nodes.
    The connected nodes are retrieved from the database based on the relationship definition in the model type.

    A NeoHyperLinkedQuerySet can be obtained when submitting targets and relationships. In this case,
    the NeoLinkedQuerySet filters all nodes from the database based on the model type,
    while collecting both all nodes connected to these fetched nodes and relationships objects.
    The relationships are retrieved from the database based on the relationship definition in the model type.

    Keys in the targets and relationships dictionaries must declare which target/relationship attribute
    defined in the model type should be used to perform a linked or hyperlinked query set and thus fetch the connected
    nodes and relationships.

    Values in the targets and relationships dictionaries will be interpreted as lists of fields
    that must be retrieved from the connected nodes and relationships objects and then loaded into NeoNodes.

    :type cls: Union[Type[DjangoNode], Type[NeoNode]]
    :type fields: List[str]
    :type targets: Dict[str, List[str]]
    :type relationships: Dict[str, List[str]]
    :type kwargs: Dict[str, str]

    :param cls: A neomodel structured node type available at the data model package
    that represents a node in the Neo4j ProTReND database
    :param fields: A list of fields that will be used to fetch the node properties and load them into a NeoNode instance
    :param targets: A dictionary of target-fields pairs that will be used to fetch the connected nodes' properties
    and load them into NeoNodes instances
    :param relationships: A dictionary of relationship-fields pairs that will be used to fetch
    the connected relationships' properties and load them into NeoNodes instances
    :param kwargs: A dictionary of query filters

    :return: It returns a NeoQuerySet, NeoLinkedQuerySet, or NeoHyperLinkedQuerySet based on the inputs,
    namely targets and relationships
    """
    if not targets:
        targets = {}

    if not relationships:
        relationships = {}

    if not targets and relationships:
        raise ValueError('Cannot fetch relationships without targets')

    query_sets = []
    for target, target_fields in targets.items():
        relationship_fields = relationships.get(target)
        query_set = get_query_set(cls=cls, fields=fields, target=target, target_fields=target_fields,
                                  relationship_fields=relationship_fields)
        query_set.filter(**kwargs)
        query_sets.append(query_set)

    if len(query_sets) == 1:
        return query_sets[0]

    query_set = add_query_sets(*query_sets)
    return query_set


# ---------------------------------------------------------
# Single Object Queries
# ---------------------------------------------------------
@raise_exception
def get_object(cls: _model_type,
               fields: List[str] = None,
               targets: Dict[str, List[str]] = None,
               relationships: Dict[str, List[str]] = None,
               **kwargs) -> Union[NeoQuerySet,
                                  NeoLinkedQuerySet,
                                  NeoHyperLinkedQuerySet]:
    """
    It builds a NeoQuerySet that retrieves a single node from the database based on the model type
    and the unique identifier provided in the query filter.
    The model label will be used in the cypher query to the database.

    The list of fields that must be fetched from the database for a given node can be used to speed up the cypher query.
    Fields' list should contain only node properties that must be fetched and loaded into a NeoNode.

    A NeoLinkedQuerySet can be obtained when submitting targets. In this case, the NeoLinkedQuerySet retrieves
    a single node based on the model type, while collecting all nodes connected to the fetched node.
    The connected nodes are retrieved from the database based on the relationship definition in the model type.

    A NeoHyperLinkedQuerySet can be obtained when submitting targets and relationships. In this case,
    the NeoLinkedQuerySet retrieves a single node from the database based on the model type,
    while collecting both all nodes connected to the fetched node and relationships objects.
    The relationships are retrieved from the database based on the relationship definition in the model type.

    Keys in the targets and relationships dictionaries must declare which target/relationship attribute
    defined in the model type should be used to perform a linked or hyperlinked query set and thus fetch the connected
    nodes and relationships.

    Values in the targets and relationships dictionaries will be interpreted as lists of fields
    that must be retrieved from the connected nodes and relationships objects and then loaded into NeoNodes.

    :type cls: Union[Type[DjangoNode], Type[NeoNode]]
    :type fields: List[str]
    :type targets: Dict[str, List[str]]
    :type relationships: Dict[str, List[str]]

    :param cls: A neomodel structured node type available at the data model package
    that represents a node in the Neo4j ProTReND database
    :param fields: A list of fields that will be used to fetch the node properties and load them into a NeoNode instance
    :param targets: A dictionary of target-fields pairs that will be used to fetch the connected nodes' properties
    and load them into NeoNodes instances
    :param relationships: A dictionary of relationship-fields pairs that will be used to fetch
    the connected relationships' properties and load them into NeoNodes instances
    :param kwargs: A dictionary of node property and value pairs

    :return: It returns a NeoQuerySet, NeoLinkedQuerySet, or NeoHyperLinkedQuerySet based on the inputs,
    namely targets and relationships
    """
    if not targets:
        targets = {}

    if not relationships:
        relationships = {}

    if not targets and relationships:
        raise ValueError('Cannot fetch relationships without targets')

    query_sets = []
    for target, target_fields in targets.items():
        relationship_fields = relationships.get(target)
        query_set = get_query_set(cls=cls, fields=fields, target=target, target_fields=target_fields,
                                  relationship_fields=relationship_fields)
        query_set.get(**kwargs)
        query_sets.append(query_set)

    if len(query_sets) == 1:
        return query_sets[0]

    query_set = add_query_sets(*query_sets)
    return query_set
