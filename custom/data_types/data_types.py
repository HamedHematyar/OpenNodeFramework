from backend.data_types import GenericStr
from backend.registry import register_data_type


@register_data_type
class NodeName(GenericStr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

