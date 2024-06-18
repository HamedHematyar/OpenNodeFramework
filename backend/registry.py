import threading

from backend.attributes import *
from backend.nodes import *
from backend.graphs import *
from backend.aggregations import *
from backend.events import *
from backend.validators import *


Lock = threading.Lock()


RegisteredNodes = {entry.__name__: entry for entry in [Node,
                                                       SumNode,
                                                       ParameterNode
                                                       ]}

RegisteredAttributes: t.Dict[str, type] = {entry.__name__: entry for entry in [GenericStr,
                                                                               GenericInt,
                                                                               GenericList,
                                                                               ]}

RegisteredPorts = {entry.__name__: entry for entry in [InputPort,
                                                       OutputPort
                                                       ]}

RegisteredCollections = {entry.__name__: entry for entry in [AttributeCollection,
                                                             PortCollection,
                                                             NodeCollection
                                                             ]}

RegisteredGraphs = {entry.__name__: entry for entry in [Graph,
                                                        ]}

RegisteredEvents = {entry.__name__: entry for entry in [PreNodeInitialized,
                                                        PostNodeInitialized,
                                                        PreNodeDeleted,
                                                        PostNodeDeleted,

                                                        PreAttributeInitialized,
                                                        PostAttributeInitialized,
                                                        PreAttributeDeleted,
                                                        PostAttributeDeleted,
                                                        PreAttributeValueChanged,
                                                        PostAttributeValueChanged,
                                                        PreAttributeLinked,
                                                        PostAttributeLinked,
                                                        PreAttributeUnlinked,
                                                        PostAttributeUnlinked,

                                                        PrePortInitialized,
                                                        PostPortInitialized,
                                                        PrePortDeleted,
                                                        PostPortDeleted,

                                                        PreGraphInitialized,
                                                        PostGraphInitialized,
                                                        PreGraphDeleted,
                                                        PostGraphDeleted,
                                                        ]}


def register_custom_attribute(cls: t.Type[BaseAttribute]) -> t.Type[BaseAttribute]:
    RegisteredAttributes.update({cls.__name__: cls})
    logger.debug(f'new attribute has been registered: {cls.__name__}')

    return cls
