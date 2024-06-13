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


InitializedNodes = {}


def register_runtime_node(instance: BaseNode, name: str):
    validate_node_name(name)

    if name in InitializedNodes:
        name = f"{name}_{len(InitializedNodes)}"

    InitializedNodes[name] = instance
    return name


def register_custom_attribute(instance: BaseAttribute) -> type:
    subclass: type = type(instance.name.capitalize(), (instance.__class__,), {})
    RegisteredAttributes.update({subclass.__name__: subclass})

    logger.debug(f"new attribute has been registered : {subclass}")
    return subclass


def register_custom_attributes():
    for entry in os.scandir("../custom/attributes"):
        loaded_attribute = AttributeSerializer().load(entry.path)
        register_custom_attribute(loaded_attribute)
