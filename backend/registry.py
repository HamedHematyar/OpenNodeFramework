import threading

from backend.data_types import *
from backend.nodes import *
from backend.aggregations import *
from backend.events import *
from backend.validators import *
from backend.ports import *


Lock = threading.Lock()


RegisteredNodes = {entry.__name__: entry for entry in [Node,
                                                       SumNode,
                                                       ParameterNode
                                                       ]}

RegisteredTypes: t.Dict[str, type] = {entry.__name__: entry for entry in [GenericStr,
                                                                          GenericInt,
                                                                          GenericList,
                                                                          ]}

RegisteredPorts = {entry.__name__: entry for entry in [GenericPort,
                                                       ]}

RegisteredCollections = {entry.__name__: entry for entry in [TypeCollection,
                                                             PortCollection,
                                                             NodeCollection
                                                             ]}

RegisteredEvents = {entry.__name__: entry for entry in [PreNodeInitialized,
                                                        PostNodeInitialized,
                                                        PreNodeDeleted,
                                                        PostNodeDeleted,

                                                        PreTypeInitialized,
                                                        PostTypeInitialized,
                                                        PreTypeDeleted,
                                                        PostTypeDeleted,
                                                        PreTypeDataChanged,
                                                        PostTypeDataChanged,

                                                        PrePortInitialized,
                                                        PostPortInitialized,
                                                        PrePortDeleted,
                                                        PostPortDeleted,

                                                        PreGraphInitialized,
                                                        PostGraphInitialized,
                                                        PreGraphDeleted,
                                                        PostGraphDeleted,
                                                        ]}


def register_custom_type(cls: t.Type[BaseType]) -> t.Type[BaseType]:
    RegisteredTypes.update({cls.__name__: cls})
    logger.debug(f'new type has been registered: {cls.__name__}')

    return cls
