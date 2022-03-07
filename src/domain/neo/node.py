from typing import List, Type, Union

from .field import NodeField, NodeRelationshipField, NodeLinkField


class BaseNode:
    def __init__(self, **kwargs):
        for attr, kwarg in kwargs.items():
            setattr(self, attr, kwarg)


class NodeMeta(type):
    def __new__(mcs,
                name,
                bases,
                namespace,
                fields: List[str] = None,
                link: str = None,
                link_fields: List[str] = None,
                rel_fields: List[str] = None):
        cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)

        if fields is None:
            fields = []

        if link_fields is None:
            link_fields = []

        if rel_fields is None:
            rel_fields = []

        # node's fields
        for field in fields:
            setattr(cls, field, NodeField(field))
        setattr(cls, 'fields', fields)

        # links' fields
        link_cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)
        for field in link_fields:
            setattr(link_cls, field, NodeField(field))
        setattr(cls, link, NodeLinkField(link, link_cls))
        setattr(cls, 'link_fields', link_fields)

        # rels' fields
        rel_cls = super(NodeMeta, mcs).__new__(mcs, name, bases, namespace)
        for field in rel_fields:
            setattr(rel_cls, field, NodeField(field))
        setattr(link_cls, 'relationship', NodeRelationshipField('relationship', rel_cls))
        setattr(cls, 'link_fields', link_fields)

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
