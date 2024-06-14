import os
import threading

from backend.attributes import *
from backend.nodes import *
from backend.graphs import *
from backend.aggregations import *
from backend.serializers import *
from backend.events import *
from backend.validators import *


Lock = threading.Lock()


RegisteredNodes = {entry.__name__: entry for entry in [Node,
                                                       SumNode,
                                                       ParameterNode
                                                       ]}

RegisteredAttributes: t.Dict[str, type] = {entry.__name__: entry for entry in [String,
                                                                               Integer,
                                                                               List,
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

RegisteredEvents = {entry.__name__: entry for entry in [NodePreInstanced,
                                                        NodePostInstanced,
                                                        NodePreInitialized,
                                                        NodePostInitialized,
                                                        NodePreRemoved,
                                                        NodePostRemoved,

                                                        AttributePreInstanced,
                                                        AttributePostInstanced,
                                                        AttributePreInitialized,
                                                        AttributePostInitialized,
                                                        AttributePreRemoved,
                                                        AttributePostRemoved,

                                                        PortPreInstanced,
                                                        PortPostInstanced,
                                                        PortPreInitialized,
                                                        PortPostInitialized,
                                                        PortPreRemoved,
                                                        PortPostRemoved,

                                                        GraphPreInstanced,
                                                        GraphPostInstanced,
                                                        GraphPreInitialized,
                                                        GraphPostInitialized,
                                                        GraphPreRemoved,
                                                        GraphPostRemoved,
                                                        ]}


def register_custom_attribute(cls: t.Type[BaseAttribute]) -> t.Type[BaseAttribute]:
    RegisteredAttributes.update({cls.__name__: cls})
    logger.debug(f'new attribute has been registered: {cls.__name__}')

    return cls
