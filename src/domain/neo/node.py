from typing import List, Type, Union

from .field import NodeField, NodeRelationshipField, NodeLinkField, DefaultField


class BaseNode:
    def __init__(self, **kwargs):
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
        raise AttributeError(f'{item} attribute not found in BaseNode')

    def add(self, other):
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


class NodeMeta(type):
    def __new__(mcs,
                name,
                bases,
                namespace,
                fields: List[str] = None,
                target: str = None,
                target_fields: List[str] = None,
                relationship_fields: List[str] = None):
        # the new source class
        cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)

        # the new source class fields
        if fields:
            for field in fields:
                setattr(cls, field, NodeField(field))
            setattr(cls, 'fields_', DefaultField('fields_', fields))

        # a new source class is created for a given target (target source)
        if target:
            link_cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)
            setattr(cls, target, NodeLinkField(target, link_cls))
            setattr(cls, 'targets_', DefaultField('targets_', [target]))

            rel_cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)
            setattr(link_cls, 'relationship_', NodeRelationshipField('relationship_', rel_cls))

            # the new source class fields for the target
            if target_fields:

                for field in target_fields:
                    setattr(link_cls, field, NodeField(field))

                setattr(link_cls, 'fields_', DefaultField('fields_', target_fields))

            # the new relationship class fields for the target
            if relationship_fields:

                for field in relationship_fields:
                    setattr(rel_cls, field, NodeField(field))

                setattr(rel_cls, 'fields_', DefaultField('fields_', relationship_fields))

        return cls

    def __init__(cls, name, bases, namespace, *args, **kwargs):
        super(NodeMeta, cls).__init__(name, bases, namespace)


def node_factory(fields: List[str] = None,
                 target: str = None,
                 target_fields: List[str] = None,
                 relationship_fields: List[str] = None) -> Union[type, Type[BaseNode]]:

    cls = NodeMeta(name='Node',
                   bases=(BaseNode,),
                   namespace={},
                   fields=fields,
                   target=target,
                   target_fields=target_fields,
                   relationship_fields=relationship_fields)
    return cls
