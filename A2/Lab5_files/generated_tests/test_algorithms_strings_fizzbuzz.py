# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.strings.fizzbuzz as module_0


def test_case_0():
    float_0 = 0.001
    with pytest.raises(ValueError):
        module_0.fizzbuzz(float_0)


def test_case_1():
    int_0 = 94
    var_0 = module_0.fizzbuzz(int_0)


@pytest.mark.xfail(strict=True)
def test_case_2():
    bool_0 = True
    var_0 = module_0.fizzbuzz_with_helper_func(bool_0)
    var_1 = module_0.fizzbuzz(bool_0)
    bool_1 = False
    var_2 = module_0.fizzbuzz_with_helper_func(bool_1)
    module_0.fizzbuzz_with_helper_func(var_2)


def test_case_3():
    int_0 = -1727
    var_0 = module_0.fb(int_0)
    assert var_0 == -1727
    var_1 = module_0.fizzbuzz_with_helper_func(var_0)
    var_2 = module_0.fb(var_0)


def test_case_4():
    bool_0 = False
    var_0 = module_0.fb(bool_0)
    assert var_0 == "FizzBuzz"
    none_type_0 = None
    with pytest.raises(TypeError):
        module_0.fizzbuzz(none_type_0)


def test_case_5():
    int_0 = 94
    var_0 = module_0.fb(int_0)
    assert var_0 == 94
    var_1 = module_0.fb(var_0)
    assert var_1 == 94


@pytest.mark.xfail(strict=True)
def test_case_6():
    str_0 = "\tQZ{+0Gk|Y;"
    module_0.fb(str_0)
