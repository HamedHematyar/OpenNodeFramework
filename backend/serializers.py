import typing as t
import json
from abc import ABC, abstractmethod

from backend import registry


class AbstractJsonSerializer(ABC):
    @abstractmethod
    def serialize(self, instance: t.Any) -> t.Dict[str, t.Any]:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def deserialize(self, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        raise NotImplementedError('this method is not implemented in subclass.')

    @abstractmethod
    def dump(self, obj: t.Any, file_path: str):
        raise NotImplementedError('this method is not implemented in subclass.')

    def load(self, file_path: str):
        raise NotImplementedError('this method is not implemented in subclass.')

    @staticmethod
    def _encode(obj) -> t.Dict[str, t.Any]:
        raise NotImplementedError('this method is not implemented in subclass.')

    @staticmethod
    def _decode(data: t.Dict[str, t.Any]) -> t.Any:
        raise NotImplementedError('this method is not implemented in subclass.')


class JsonSerializer(AbstractJsonSerializer):
    def serialize(self, instance: t.Any) -> t.Dict[str, t.Any]:
        return self._encode(instance)

    def deserialize(self, data: t.Dict[str, t.Any], *args, **kwargs) -> t.Any:
        return self._decode(data)

    def dump(self, obj, file_path, *args, **kwargs):
        with open(file_path, 'w') as file:
            json.dump(obj, file, default=self._encode, *args, **kwargs)

    def load(self, file_path, *args, **kwargs):
        with open(file_path, 'r') as file:
            return self._decode(json.load(file, *args, **kwargs))


class AttributeSerializer(JsonSerializer):

    def deserialize(self, data: t.Dict[str, t.Any], node=None, *args, **kwargs):
        instance = super().deserialize(data)
        if node:
            instance.node = node

        return instance

    @staticmethod
    def _encode(obj):
        data = {'class': obj.__class__.__name__,
                'name': obj.name,
                'value': obj.value}

        return data

    @staticmethod
    def _decode(data):
        instance = registry.RegisteredAttributes[data.pop('class')](*data.values())

        return instance


class AttributeCollectionSerializer(JsonSerializer):

    def deserialize(self, data: t.Dict[str, t.Any], node=None, *args, **kwargs) -> t.Any:
        instance = super().deserialize(data)

        if node:
            instance.node = node

            for entry in instance.node.attributes.values():
                entry.node = node

        return instance

    @staticmethod
    def _encode(obj):
        entries = []
        for key, attr in obj.items():
            entries.append(AttributeSerializer().serialize(attr))

        data = {'class': obj.__class__.__name__,
                'entries': entries}

        return data

    @staticmethod
    def _decode(data):
        instance = registry.RegisteredCollections[data.pop('class')]()

        for entry_data in data['entries']:
            instance.add(AttributeSerializer().deserialize(entry_data))

        return instance


class PortSerializer(JsonSerializer):

    def deserialize(self, data: t.Dict[str, t.Any], node=None, *args, **kwargs) -> t.Any:
        instance = super().deserialize(data)

        if node:
            instance.node = node

        # TODO deserialize port connections
        return instance

    @staticmethod
    def _encode(obj):
        data = {'class': obj.__class__.__name__,
                'mode': obj.mode.value,
                'name': obj.name,
                'connections': []}

        # TODO serialize port connections
        return data

    @staticmethod
    def _decode(data):
        from backend.enums import PortType
        mode = getattr(PortType, data['mode'].capitalize())
        instance = registry.RegisteredPorts[data.pop('class')](data['name'], mode)

        # TODO deserialize port connections
        return instance


class PortCollectionSerializer(JsonSerializer):

    def deserialize(self, data: t.Dict[str, t.Any], node=None, *args, **kwargs) -> t.Any:
        instance = super().deserialize(data)

        if node:
            instance.node = node

            for entry in instance:
                entry.node = node

        return instance

    @staticmethod
    def _encode(obj):
        entries = []
        for entry in obj:
            entries.append(PortSerializer().serialize(entry))

        data = {'class': obj.__class__.__name__,
                'entries': entries}

        return data

    @staticmethod
    def _decode(data):
        instance = registry.RegisteredCollections[data.pop('class')]()

        for entry_data in data['entries']:
            instance.append(PortSerializer().deserialize(entry_data))

        return instance


class NodeSerializer(JsonSerializer):

    def deserialize(self, data: t.Dict[str, t.Any], graph=None, *args, **kwargs) -> t.Any:
        instance = super().deserialize(data)

        if graph:
            instance.graph = graph

        return instance

    @staticmethod
    def _encode(obj):
        data = {'class': obj.__class__.__name__,
                'attributes': AttributeCollectionSerializer().serialize(obj.attributes),
                'inputs': PortCollectionSerializer().serialize(obj.inputs),
                'outputs': PortCollectionSerializer().serialize(obj.outputs)}

        return data

    @staticmethod
    def _decode(data):
        node = registry.RegisteredNodes[data.pop('class')]()

        node.attributes = AttributeCollectionSerializer().deserialize(data['attributes'], node)
        node.inputs = PortCollectionSerializer().deserialize(data['inputs'], node)
        node.output = PortCollectionSerializer().deserialize(data['outputs'], node)

        return node


class NodeCollectionSerializer(JsonSerializer):

    def deserialize(self, data: t.Dict[str, t.Any], graph=None, *args, **kwargs) -> t.Any:
        instance = super().deserialize(data)

        if graph:
            instance.graph = graph

            for entry in instance:
                entry.graph = graph

        return instance

    @staticmethod
    def _encode(obj):
        entries = []
        for entry in obj:
            entries.append(NodeSerializer().serialize(entry))

        data = {'class': obj.__class__.__name__,
                'entries': entries}

        return data

    @staticmethod
    def _decode(data):
        instance = registry.RegisteredCollections[data.pop('class')]()

        for entry in data['entries']:
            instance.append(NodeSerializer().deserialize(entry))

        return instance


class GraphSerializer(JsonSerializer):

    @staticmethod
    def _encode(obj, data=None):
        data = data or {}
        data.update({'graphs': {obj.name: {'class': obj.__class__.__name__,
                                           'name': obj.name,
                                           'nodes': NodeCollectionSerializer().serialize(obj.nodes)}}})

        for graph in obj.graphs:
            data['graphs'][obj.name] = GraphSerializer._encode(graph, data['graphs'][obj.name])

        return data

    @staticmethod
    def _decode(data, parent=None):

        for graph_name, graph_data in data.get('graphs', {}).items():
            graph = registry.RegisteredGraphs[graph_data.pop('class')](graph_name)
            graph.nodes = NodeCollectionSerializer().deserialize(graph_data['nodes'], parent)

            sub_graph = GraphSerializer._decode(graph_data, graph)
            if sub_graph:
                graph.graphs.append(sub_graph)

            return graph
