from typing import Type, List, Union

from django_neomodel import DjangoNode


class LazyProperty:

    def __init__(self, name):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if instance is None:
            return self

        instance.__dict__[self.name] = value


class LazyNodeMeta(type):
    def __new__(mcs, name, bases, namespace, properties=None):
        if properties is None:
            properties = []

        cls = super(LazyNodeMeta, mcs).__new__(mcs, name, bases, namespace)

        for attr in properties:
            setattr(cls, attr, LazyProperty(attr))
        setattr(cls, 'properties', properties)
        return cls

    def __init__(cls, name, bases, namespace, *args, **kwargs):
        super(LazyNodeMeta, cls).__init__(name, bases, namespace)


class LazyNode:

    def __init__(self, *args, **kwargs):

        if args:
            for arg, attr in zip(args, self.meta):
                setattr(self, attr, arg)

        if kwargs:
            for attr, kwarg in kwargs.items():
                setattr(self, attr, kwarg)

    def __getattr__(self, item):
        return


def build_lazy_node(node: Type[DjangoNode], properties: List[str]) -> Union[type, LazyNodeMeta]:
    name = f'Lazy{node.__label__}'
    bases = (LazyNode,)
    cls = LazyNodeMeta(name=name, bases=bases, namespace={}, properties=properties)
    return cls
