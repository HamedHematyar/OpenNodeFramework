import pathlib

from backend.data_types import GenericInt
from backend.meta import InstanceManager


def test():
    """
    >>> # create an int type with no data
    >>> constant = GenericInt()
    >>> print(constant.serialize()) # doctest: +ELLIPSIS
    {...}

    >>> # test default value fallback
    >>> constant.data() == constant.default
    True

    >>> # delete before override
    >>> constant.delete()

    >>> # create an int type
    >>> constant = GenericInt(data=30)

    >>> # get entity id
    >>> constant_id = constant.get_id()

    >>> # make sure its tracked
    >>> constant.get_id() in InstanceManager().instances()
    True

    >>> InstanceManager().get_instance(constant_id) is constant
    True

    >>> # test data using data() method
    >>> constant.data()
    30

    >>> # test data using get_data() method
    >>> constant.get_data()
    30

    >>> # set valid data and verify
    >>> constant.set_data(40)
    True

    >>> constant.data()
    40

    >>> # set invalid data and verify
    >>> constant.set_data('hello')
    False

    >>> constant.data()
    40

    >>> # test multi type support
    >>> constant.set_data(13.5)
    True

    >>> constant.data()
    13

    >>> # direct data validation
    >>> constant.validate_data('hello')
    False

    >>> constant.validate_data(12)
    True

    >>> constant.del_data()
    >>> constant.data() == constant.default
    True

    >>> constant.set_data(75)
    True

    >>> constant.data()
    75

    >>> # check dumps data
    >>> print(constant.dumps(indent=4)) # doctest: +ELLIPSIS
    {...}

    >>> # check serialized data
    >>> serialized_constant = constant.serialize()
    >>> print(serialized_constant) # doctest: +ELLIPSIS
    {...}

    >>> deserialized_constant = GenericInt.deserialize(serialized_constant)
    >>> constant.data()
    75

    >>> # test if the loaded one is a new one
    >>> deserialized_constant.get_id() == constant.get_id()
    False

    >>> path = pathlib.Path("../dump/types/constant.json")
    >>> constant.dump(path, indent=4)

    >>> path.is_file()
    True

    >>> loaded_constant = GenericInt.load(path)
    >>> constant.data()
    75

    >>> # test if the loaded one is a new one
    >>> loaded_constant.get_id() == constant.get_id()
    False

    >>> print(InstanceManager().instances()) # doctest: +ELLIPSIS
    {...}

    >>> len(InstanceManager().instances())
    3

    >>> constant.delete()
    >>> deserialized_constant.delete()
    >>> loaded_constant.delete()

    >>> len(InstanceManager().instances())
    0
    """


if __name__ == '__main__':
    test()
