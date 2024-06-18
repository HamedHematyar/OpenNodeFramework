import gc
from backend.attributes import GenericInt
from backend.meta import InstanceManager
from backend.events import *


def attribute_pre_init(*args, **kwargs):
    print(f'attribute_pre_init : {args} {kwargs}')


def attribute_post_init(*args, **kwargs):
    print(f'attribute_post_init : {args} {kwargs}')


def attribute_pre_removed(*args, **kwargs):
    print(f'attribute_pre_removed : {args} {kwargs}')


def attribute_post_removed(*args, **kwargs):
    print(f'attribute_post_removed : {args} {kwargs}')


def pre_attribute_value_changed(*args, **kwargs):
    print(f'pre_attribute_value_changed : {args} {kwargs}')


def post_attribute_value_changed(*args, **kwargs):
    print(f'post_attribute_value_changed : {args} {kwargs}')


def pre_attribute_linked(*args, **kwargs):
    print(f'pre_attribute_linked : {args} {kwargs}')


def post_attribute_linked(*args, **kwargs):
    print(f'post_attribute_linked : {args} {kwargs}')


def pre_attribute_unlinked(*args, **kwargs):
    print(f'pre_attribute_unlinked : {args} {kwargs}')


def post_attribute_unlinked(*args, **kwargs):
    print(f'post_attribute_unlinked : {args} {kwargs}')


if __name__ == '__main__':
    EventManager().register_callback(PreAttributeDeleted, attribute_pre_removed)
    EventManager().register_callback(PostAttributeDeleted, attribute_post_removed)

    EventManager().register_callback(PreAttributeInitialized, attribute_pre_init)
    EventManager().register_callback(PostAttributeInitialized, attribute_post_init)

    EventManager().register_callback(PreAttributeValueChanged, pre_attribute_value_changed)
    EventManager().register_callback(PostAttributeValueChanged, post_attribute_value_changed)

    EventManager().register_callback(PreAttributeLinked, pre_attribute_linked)
    EventManager().register_callback(PostAttributeLinked, post_attribute_linked)

    EventManager().register_callback(PreAttributeUnlinked, pre_attribute_unlinked)
    EventManager().register_callback(PostAttributeUnlinked, post_attribute_unlinked)

    driver_attr = GenericInt(name='driver', value=30)
    print(driver_attr.dumps(indent=4))

    driven_attr = GenericInt(name='constant', value=10)
    driven_attr.set_link(driver_attr)
    print(driven_attr.dumps(indent=4))

    serialized = driven_attr.serialize()
    print(serialized)

    deserialized = GenericInt.deserialize(serialized, relations=True)
    print(deserialized.dumps(indent=4))

    print(len(InstanceManager().instances()))
