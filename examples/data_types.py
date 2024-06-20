import pathlib

from backend.data_types import GenericInt
from backend.meta import InstanceManager


if __name__ == '__main__':
    # create an int type with no data
    constant = GenericInt()

    # test default value fallback
    assert constant.data() == constant.default

    # delete before override
    constant.delete()

    # create an int type
    constant = GenericInt(data=30)

    # get entity id
    constant_id = constant.get_id()
    print(constant_id)

    # make sure its tracked
    assert constant.get_id() in InstanceManager().instances()
    assert InstanceManager().get_instance(constant_id) is constant

    # test data using data() method
    assert constant.data() == 30

    # test data using get_data() method
    assert constant.get_data() == 30

    # set valid data and verify
    constant.set_data(40)
    assert constant.data() == 40

    # set invalid data and verify
    constant.set_data('hello')
    assert constant.data() == 40

    # test multi type support
    constant.set_data(13.5)
    assert constant.data() == 13

    # direct data validation
    assert constant.validate_data('hello') is False
    assert constant.validate_data(12) is True

    constant.del_data()
    assert constant.data() == constant.default

    constant.set_data(75)
    assert constant.data() == 75

    # check dumps data
    print(constant.dumps(indent=4))

    # check serialized data
    serialized_constant = constant.serialize()
    print(serialized_constant)

    deserialized_constant = GenericInt.deserialize(serialized_constant)
    assert constant.data() == 75

    # test if the loaded one is a new one
    assert deserialized_constant.get_id() != constant.get_id()

    path = pathlib.Path("../dump/types/constant.json")
    constant.dump(path, indent=4)

    assert path.is_file()

    loaded_constant = GenericInt.load(path)
    assert constant.data() == 75

    # test if the loaded one is a new one
    assert loaded_constant.get_id() != constant.get_id()

    print(InstanceManager().instances())
    assert len(InstanceManager().instances()) == 3

    constant.delete()
    deserialized_constant.delete()
    loaded_constant.delete()

    assert len(InstanceManager().instances()) == 0
