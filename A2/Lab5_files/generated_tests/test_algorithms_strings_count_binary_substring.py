# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.strings.count_binary_substring as module_0


def test_case_0():
    bool_0 = True
    tuple_0 = (bool_0, bool_0)
    var_0 = module_0.count_binary_substring(tuple_0)
    assert var_0 == 0


@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = True
    module_0.count_binary_substring(bool_0)


@pytest.mark.xfail(strict=True)
def test_case_2():
    bool_0 = True
    bytes_0 = b"\xfd\xaf\x1f\xd2\xc7#Z\xfa\xff\xa9"
    tuple_0 = (bool_0, bytes_0)
    var_0 = module_0.count_binary_substring(tuple_0)
    assert var_0 == 1
    dict_0 = {tuple_0: tuple_0, var_0: bool_0, bool_0: var_0}
    module_0.count_binary_substring(dict_0)
