from typing import List, Type, Union

from .field import NodeField, NodeRelationshipField, NodeLinkField, DefaultField


class NeoNodeMeta(type):
    """
    Metaclass for dynamic building of NeoNode classes.
    NeoNodeMeta is used in the node factoring method to create dynamic NeoNode classes,
    according to the requested fields, targets and relationships.
    NeoNode classes can then be used to hold nodes' properties, nodes' properties and connected nodes' properties, and
    nodes' properties, connected nodes' properties and connected relationships' properties
    """
    def __new__(mcs,
                name,
                bases,
                namespace,
                fields: List[str] = None,
                target: str = None,
                target_fields: List[str] = None,
                relationship_fields: List[str] = None):
        # Creating the new NeoNode class
        cls = super(NeoNodeMeta, mcs).__new__(mcs, name, bases, namespace)

        # Adding NeoNode data descriptors based on the requested fields which can load the nodes' properties
        if fields:
            for field in fields:
                setattr(cls, field, NodeField(field))
            setattr(cls, 'fields_', DefaultField('fields_', fields))

        if target:
            # Creating the new target NeoNode class
            target_cls = super(NeoNodeMeta, mcs).__new__(mcs, name, bases, namespace)

            # Adding NeoNode data descriptors based on the requested target
            # which can load the new target NeoNode instance
            setattr(cls, target, NodeLinkField(target, target_cls))
            setattr(cls, 'targets_', DefaultField('targets_', [target]))

            # Creating the new relationship NeoNode class
            relationship_cls = super(NeoNodeMeta, mcs).__new__(mcs, name, bases, namespace)

            # Adding NeoNode data descriptors to the target NeoNode class based on the requested relationship
            # which can load the new relationship NeoNode instance
            setattr(target_cls, 'relationship_', NodeRelationshipField('relationship_', relationship_cls))

            # Adding NeoNode data descriptors to the target NeoNode class based on the requested target fields
            # which can load the connected nodes' properties
            if target_fields:

                for field in target_fields:
                    setattr(target_cls, field, NodeField(field))

                setattr(target_cls, 'fields_', DefaultField('fields_', target_fields))

            # Adding NeoNode data descriptors to the relationship NeoNode class
            # based on the requested relationship fields which can load the connected relationship' properties
            if relationship_fields:

                for field in relationship_fields:
                    setattr(relationship_cls, field, NodeField(field))

                setattr(relationship_cls, 'fields_', DefaultField('fields_', relationship_fields))

        return cls

    def __init__(cls, name, bases, namespace, *args, **kwargs):
        super(NeoNodeMeta, cls).__init__(name, bases, namespace)


class NeoNode:

    def __init__(self, **kwargs):
        """
        The NeoNode object is generated dynamically by the NeoNodeMeta metaclass.
        Hence, NeoNode classes can actually be very different from each other, as these are tailor-made NeoNode classes.

        A NeoNode instance uses the data-descriptors added to the NeoNode class upon class generation in the metaclass.
        Hence, NeoNode instances have different attributes from each other.

        A NeoNode can be instantiated with a dictionary of attribute name to attribute value pairs.
        These attributes will be dynamically loaded into the NeoNode instance using the data descriptors

        :param kwargs: A dictionary of attribute name and attribute value pairs
        """
        for attr, kwarg in kwargs.items():
            setattr(self, attr, kwarg)

    def __str__(self):
        if hasattr(self, 'fields_'):
            fields = ', '.join(f'{field}: {getattr(self, field)}' for field in self.fields_)
            return f'{{{fields}}}'

        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, item):
        raise AttributeError(f'{item} attribute not found in NeoNode')

    def add(self, other):
        """
        NeoNode instances can be merged/concatenated with other NeoNodes.
        Fields, targets and relationships available in the other NeoNode instance
        but not present in this NeoNode instance will be loaded into this instance.

        Note that, this method does not yield a new NeoNode instance.

        :param other: Other NeoNode instance
        :return: This NeoNode instance
        """
        if hasattr(self, 'fields_') and hasattr(other, 'fields_'):

            for field in other.fields_:
                if field not in self.fields_:
                    value = getattr(other, field)
                    setattr(self, field, value)
                    self.fields_.append(field)

        if hasattr(other, 'targets_'):

            if not hasattr(self, 'targets_'):
                setattr(self, 'targets_', [])

            for target in other.targets_:
                if target not in self.targets_:
                    value = getattr(other, target)
                    setattr(self, target, value)
                    self.targets_.append(target)

        return self


def node_factory(fields: List[str] = None,
                 target: str = None,
                 target_fields: List[str] = None,
                 relationship_fields: List[str] = None) -> Union[type, Type[NeoNode]]:

    """
    The node factory calls NeoNodeMeta to create dynamic NeoNode classes,
    according to the requested fields, targets and relationships.

    NeoNode classes can then be used to hold nodes' properties, nodes' properties and connected nodes' properties, and
    nodes' properties, connected nodes' properties and connected relationships' properties

    :type fields: List[str]
    :type target: str
    :type target_fields: List[str]
    :type relationship_fields: List[str]

    :param fields: A list of fields that will be used to fetch the node properties and load them into a NeoNode instance
    :param target: The relationship attribute name that will be used to fetch the connected nodes
    :param target_fields: A list of fields that will be used to fetch the connected nodes' properties
    and load them into a NeoNode instances
    :param relationship_fields: A list of fields that will be used to fetch the connected relationships' properties
    and load them into a NeoNode instances

    :return: It returns a new NeoNode class
    """

    cls = NeoNodeMeta(name='Node',
                      bases=(NeoNode, ),
                      namespace={},
                      fields=fields,
                      target=target,
                      target_fields=target_fields,
                      relationship_fields=relationship_fields)
    return cls
