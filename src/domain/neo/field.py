class NodeField:

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


class NodeLinkField:

    def __init__(self, name, link_cls):
        self.name = name
        self.link_cls = link_cls

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if instance is None:
            return self

        if not value:
            value = []

        values = [self.link_cls(**kwargs) for kwargs in value]
        instance.__dict__[self.name] = values


class NodeRelationshipField:

    def __init__(self, name, rel_cls):
        self.name = name
        self.rel_cls = rel_cls

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if instance is None:
            return self

        if not value:
            value = {}

        value = self.rel_cls(**value)
        instance.__dict__[self.name] = value