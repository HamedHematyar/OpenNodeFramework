import json
import copy
import pathlib
from collections.abc import MutableMapping

from backend.abstracts import (AbstractType,
                               AbstractNode,
                               AbstractEntitySerializer,
                               EntityType)
from backend.events import *
from backend.validators import *


class EntitySerializer(AbstractEntitySerializer):
    serializable_attributes = []
    relation_attributes = []

    def serialize(self) -> t.Dict[str, t.Any]:
        return self._encode()

    @classmethod
    def deserialize(cls, data, **kwargs) -> t.Any:
        return cls._decode(copy.deepcopy(data), **kwargs)

    def dump(self, file_path: pathlib.Path, *args, **kwargs):
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path.absolute().as_posix(), 'w') as file:
            json.dump(self, file, default=self._encode, *args, **kwargs)

    def dumps(self, **kwargs):
        return json.dumps(self._encode(), **kwargs)

    @classmethod
    def load(cls, file_path: pathlib.Path, *args, **kwargs):
        with open(file_path.absolute().as_posix(), 'r') as file:
            return cls._decode(json.load(file), *args, **kwargs)

    def _encode(self, *args, **kwargs) -> t.Dict[str, t.Any]:
        data = {}

        for key in self.serializable_attributes:
            data.update(getattr(self, f'get_{key}')(serialize=True))

        return data

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any], relations=False) -> t.Any:
        for key in cls.relation_attributes:
            data.update(getattr(cls, f'deserialize_{key}')(data.pop(key)))

        instance = cls(**data)
        return instance


class DictCollection(MutableMapping):

    def __init__(self, **kwargs):
        self._internal_data = {}

        self.update(**kwargs)

    def __getitem__(self, key):
        return self._internal_data[key]

    def __setitem__(self, key, value):
        if not self.validate_item(value):
            return False

        self._internal_data[key] = value
        return True

    def __delitem__(self, key):
        del self._internal_data[key]

    def __iter__(self):
        return iter(self._internal_data)

    def __len__(self):
        return len(self._internal_data)

    def __repr__(self):
        return f'{self.__class__.__name__}({self._internal_data})'

    def get_items(self, serialize=False):
        if serialize:
            return {key: value.serialize() for key, value in self.items()}

        return self.items()

    def set_items(self, items: t.Iterable):
        if not self.validate_items(items):
            return False

        self.update(items)
        return True

    def del_items(self):
        self.clear()

    def validate_items(self, items):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def validate_item(self, item):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class CustomDictCollection(EntitySerializer, DictCollection):
    valid_types = tuple()
    validate_uniqueness = True

    serializable_attributes = ['class',
                               'items']

    def get_class(self, serialize=False):
        if serialize:
            return {'class': self.__class__.__name__}

        return self.__class__

    def validate_item(self, item):
        if not isinstance(item, self.valid_types):
            logger.warning(f'{self.__class__.__name__} item value must be of type {self.valid_types} : {item}')
            return False

        if self.validate_uniqueness and item in self.values():
            logger.warning(f'{item} is already present in the collection')
            return False

        return True

    def validate_items(self, items):
        for item in items.values():
            if not self.validate_item(item):
                return False

        return True


class BaseType(EntitySerializer, AbstractType):
    serializable_attributes = ['class',
                               'type',
                               'id',
                               'data']

    @register_events_decorator([PreTypeInitialized, PostTypeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')
        self._data: t.Optional[str] = None

        init_data = kwargs.get('data', self.default)
        if init_data is not None:
            self.set_data(init_data)

    @register_events_decorator([PreTypeDeleted, PostTypeDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return {'class': self.__class__.__name__}

        return self.__class__

    def get_type(self, serialize=False):
        if serialize:
            return {'type': self.entity_type.value}

        return self.entity_type.value

    def get_id(self, serialize=False):
        if serialize:
            return {'id': self._id}

        return self._id

    def data(self):
        return self.get_data()

    def get_data(self, serialize=False):
        if serialize:
            return {'data': self._data}

        return self._data

    @register_events_decorator([PreTypeDataChanged, PostTypeDataChanged])
    def set_data(self, data):
        if not self.validate_data(data):
            return False

        self._data = data
        return True

    def del_data(self):
        self._data = self.default

    def validate_data(self, data):
        if not isinstance(data, self.valid_types):
            logger.warning(
                f'{self.__class__} attribute value must be an instance of {self.valid_types} not {type(data)}.')
            return False

        return True

    @classmethod
    def _decode(cls, data: t.Dict[str, t.Any], relations=False) -> t.Any:
        from backend.meta import InstanceManager
        instance = InstanceManager().get_instance(data['id'])

        return instance or cls(**data)


class BaseNode(EntitySerializer, AbstractNode):
    serializable_attributes = ['class',
                               'type',
                               'id',
                               'attributes',
                               'inputs',
                               'outputs']

    relation_attributes = ['attributes',
                           'inputs',
                           'outputs']

    @register_events_decorator([PreNodeInitialized, PostNodeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._attributes = None
        self._inputs = None
        self._outputs = None

        attributes = kwargs.pop('attributes', {})
        self.set_attributes(attributes or self.init_attributes())

        inputs = kwargs.pop('inputs', {})
        self.set_inputs(inputs or self.init_inputs())

        outputs = kwargs.pop('outputs', {})
        self.set_outputs(outputs or self.init_outputs())

        self.populate_data(**kwargs)

    def init_attributes(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def init_inputs(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def init_outputs(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def populate_data(self, **kwargs):
        for key, value in kwargs.items():
            if self.attributes.get(key):
                self.attributes[key].attributes['value'].set_data(value)

    @register_events_decorator([PreNodeDeleted, PostNodeDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return {'class': self.__class__.__name__}

        return self.__class__

    def get_type(self, serialize=False):
        if serialize:
            return {'type': self.entity_type.value}

        return self.entity_type.value

    def get_id(self, serialize=False):
        if serialize:
            return {'id': self._id}

        return self._id

    @property
    def attributes(self):
        return self.get_attributes()

    def get_attributes(self, serialize=False):
        if serialize:
            return {'attributes': self._attributes.serialize()}

        return self._attributes

    def set_attributes(self, attributes):
        if not self.validate_attributes(attributes):
            return False

        self._attributes = attributes
        return True

    def del_attributes(self):
        self._attributes.clear()

    def validate_attributes(self, attributes):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @classmethod
    def deserialize_attributes(cls, data):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @property
    def inputs(self):
        return self.get_inputs()

    def get_inputs(self, serialize=False):
        if serialize:
            return {'inputs': self._inputs.serialize()}

        return self._inputs

    def set_inputs(self, inputs):
        if not self.validate_inputs(inputs):
            return False

        self._inputs = inputs
        return True

    def del_inputs(self):
        self._inputs.clear()

    def validate_inputs(self, inputs):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @classmethod
    def deserialize_inputs(cls, data):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @property
    def outputs(self):
        return self.get_outputs()

    def get_outputs(self, serialize=False):
        if serialize:
            return {'outputs': self._outputs.serialize()}

        return self._outputs

    def set_outputs(self, outputs):
        if not self.validate_outputs(outputs):
            return False

        self._outputs = outputs
        return True

    def del_outputs(self):
        self._outputs.clear()

    def validate_outputs(self, outputs):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @classmethod
    def deserialize_outputs(cls, data):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def data(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class BasePortNode(EntitySerializer, AbstractNode):
    entity_type = EntityType.Port

    serializable_attributes = ['class',
                               'type',
                               'id',
                               'attributes']

    relation_attributes = ['attributes']

    @register_events_decorator([PreNodeInitialized, PostNodeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._attributes = None

        attributes = kwargs.pop('attributes', {})
        self.set_attributes(attributes or self.init_attributes())

        self.populate_data(**kwargs)

    def init_attributes(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def populate_data(self, **kwargs):
        for key, value in kwargs.items():
            if self.attributes.get(key):
                self.attributes[key].set_data(value)

    @register_events_decorator([PreNodeDeleted, PostNodeDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return {'class': self.__class__.__name__}

        return self.__class__

    def get_type(self, serialize=False):
        if serialize:
            return {'type': self.entity_type.value}

        return self.entity_type.value

    def get_id(self, serialize=False):
        if serialize:
            return {'id': self._id}

        return self._id

    @property
    def attributes(self):
        return self.get_attributes()

    def get_attributes(self, serialize=False):
        if serialize:
            return {'attributes': self._attributes.serialize()}

        return self._attributes

    def set_attributes(self, attributes):
        if not self.validate_attributes(attributes):
            return False

        self._attributes = attributes
        return True

    def del_attributes(self):
        self._attributes.clear()

    def validate_attributes(self, attributes):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @classmethod
    def deserialize_attributes(cls, data):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def data(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')


class BaseAttributeNode(EntitySerializer, AbstractNode):
    entity_type = EntityType.Attribute

    serializable_attributes = ['class',
                               'type',
                               'id',
                               'attributes']

    relation_attributes = ['attributes']

    @register_events_decorator([PreNodeInitialized, PostNodeInitialized])
    def __init__(self, **kwargs):
        self._id = kwargs.pop('id')

        self._attributes = None

        attributes = kwargs.pop('attributes', {})
        self.set_attributes(attributes or self.init_attributes())

        self.populate_data(**kwargs)

    def init_attributes(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def populate_data(self, **kwargs):
        for key, value in kwargs.items():
            if self.attributes.get(key):
                self.attributes[key].set_data(value)

    @register_events_decorator([PreNodeDeleted, PostNodeDeleted])
    def delete(self):
        from backend.meta import InstanceManager
        InstanceManager().remove_instance(self)

        del self

    def get_class(self, serialize=False):
        if serialize:
            return {'class': self.__class__.__name__}

        return self.__class__

    def get_type(self, serialize=False):
        if serialize:
            return {'type': self.entity_type.value}

        return self.entity_type.value

    def get_id(self, serialize=False):
        if serialize:
            return {'id': self._id}

        return self._id

    @property
    def attributes(self):
        return self.get_attributes()

    def get_attributes(self, serialize=False):
        if serialize:
            return {'attributes': self._attributes.serialize()}

        return self._attributes

    def set_attributes(self, attributes):
        if not self.validate_attributes(attributes):
            return False

        self._attributes = attributes
        return True

    def del_attributes(self):
        self._attributes.clear()

    def validate_attributes(self, attributes):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    @classmethod
    def deserialize_attributes(cls, data):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')

    def data(self):
        raise NotImplementedError('This method is not implemented and must be defined in the subclass.')
