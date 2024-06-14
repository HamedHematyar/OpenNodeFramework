from backend.attributes import GenericStr
from backend.registry import register_custom_attribute


@register_custom_attribute
class NodeName(GenericStr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

