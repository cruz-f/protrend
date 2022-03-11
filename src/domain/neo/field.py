# -----------------------------------------------
# NeoNode DESCRIPTORS
# -----------------------------------------------
class DefaultField:

    def __init__(self, name, default=None):
        """
        Default field stores a default value for the NeoNode instance attribute lookup.
        At the first lookup if the attribute value is not present in the instance dict, the default field adds the
        default value received upon instantiation and class formulation

        :param name:
        :param default:
        """
        self.name = name
        self.default = default

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.name not in instance.__dict__:
            default = list(self.default)
            instance.__dict__[self.name] = default

        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if instance is None:
            return self

        instance.__dict__[self.name] = value


class NodeField:

    def __init__(self, name):
        """
        It is a simple data-descriptor that will retrieve NeoNode instance attributes, namely the NeoNode fields

        :param name:
        """
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

    def __init__(self, name, target_cls):
        """
        It is simple data-descriptor that will retrieve the NeoNode instance relationships.
        Each relationship is composed of a list of other NeoNode instances
        which hold the target nodes connected to the source node

        The data-descriptor is instantiated with the target NeoNode class formulation. This class can be used to create
        the NeoNode instances of the connected nodes upon setting the node attribute.

        :param name:
        :param target_cls:
        """
        self.name = name
        self.target_cls = target_cls

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

        values = [self.target_cls(**kwargs) for kwargs in value]
        instance.__dict__[self.name] = values


class NodeRelationshipField:

    def __init__(self, name, relationship_cls):
        """
        It is a simple data-descriptor but for relationships. It is similar to the NodeLinkFields,
        but this data-descriptor is used to register the relationship attribute in the NeoNode instances of the
        connected nodes.
        This data-descriptor is responsible for getting and setting the properties of the relationships
        :param name:
        :param relationship_cls:
        """
        self.name = name
        self.relationship_cls = relationship_cls

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

        value = self.relationship_cls(**value)
        instance.__dict__[self.name] = value
