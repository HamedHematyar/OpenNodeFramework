from backend.data_types import GenericStr
from backend.registry import register_custom_type


@register_custom_type
class NodeName(GenericStr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

