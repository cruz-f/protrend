from typing import List, Type, Union

from .field import NodeField, NodeRelationshipField, NodeLinkField


class BaseNode:
    def __init__(self, **kwargs):
        for attr, kwarg in kwargs.items():
            setattr(self, attr, kwarg)

    def __str__(self):
        if hasattr(self, 'fields'):
            fields = ', '.join(f'{field}: {getattr(self, field)}' for field in self.fields)
            return f'{{{fields}}}'

        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()


class NodeMeta(type):
    def __new__(mcs,
                name,
                bases,
                namespace,
                fields: List[str] = None,
                link: str = None,
                link_fields: List[str] = None,
                rel_fields: List[str] = None):
        # the new node class
        cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)

        # the new node class fields
        if fields is not None:
            for field in fields:
                setattr(cls, field, NodeField(field))
            setattr(cls, 'fields', fields)

        # a new node class is created for a given link (target node)
        if link is not None:
            link_cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)
            setattr(cls, link, NodeLinkField(link, link_cls))
            setattr(cls, 'link_fields', link_fields)

            rel_cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)
            setattr(link_cls, 'relationship', NodeRelationshipField('relationship', rel_cls))
            setattr(cls, 'rel_fields', rel_fields)

            # the new node class fields for the link
            if link_fields is not None:

                for field in link_fields:
                    setattr(link_cls, field, NodeField(field))

                setattr(link_cls, 'fields', link_fields)

            # the new relationship class fields for the link
            if rel_fields is not None:

                for field in rel_fields:
                    setattr(rel_cls, field, NodeField(field))

                setattr(rel_cls, 'fields', rel_fields)

        return cls

    def __init__(cls, name, bases, namespace, *args, **kwargs):
        super(NodeMeta, cls).__init__(name, bases, namespace)


def node_factory(fields: List[str] = None,
                 link: str = None,
                 link_fields: List[str] = None,
                 rel_fields: List[str] = None) -> Union[type, Type[BaseNode]]:
    cls = NodeMeta(name='Node',
                   bases=(BaseNode,),
                   namespace={},
                   fields=fields,
                   link=link,
                   link_fields=link_fields,
                   rel_fields=rel_fields)
    return cls
