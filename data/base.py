from django_neomodel import DjangoNode
from neomodel import UniqueIdProperty, StringProperty, DateTimeProperty


class BaseNode(DjangoNode):
    __abstract_node__ = True

    uid = UniqueIdProperty()
    protrend_id = StringProperty(required=True, unique_index=True)
    created = DateTimeProperty(default_now=True)
    updated = DateTimeProperty(default_now=True)

    identifying_property = 'protrend_id'
    header = 'PRT'
    entity = 'PRT'

    class Meta:
        app_label = 'data'
        order_by = ['protrend_id']
