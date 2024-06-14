from backend.attributes import String
from backend.registry import register_custom_attribute


@register_custom_attribute
class NodeName(String):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

