from django_neomodel import DjangoNode
from neomodel import UniqueIdProperty, StringProperty, DateTimeProperty

from constants import help_text


class BaseNode(DjangoNode):
    __abstract_node__ = True

    uid = UniqueIdProperty()
    protrend_id = StringProperty(required=True, unique_index=True, help_text=help_text.protrend_id)
    created = DateTimeProperty(default_now=True, help_text=help_text.created)
    updated = DateTimeProperty(default_now=True, help_text=help_text.updated)

    class Meta:
        app_label = 'data'
        order_by = ['protrend_id']
