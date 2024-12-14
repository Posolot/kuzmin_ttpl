import pytest
from ..main.hashmap import SpecialDict, InvalidConditionException


def test_iloc():
    data = SpecialDict({
        "value1": 1,
        "value2": 2,
        "value3": 3,
        "1": 10,
        "2": 20,
        "3": 30,
        "1, 5": 100,
        "5, 5": 200,
        "10, 5": 300
    })

    assert data.iloc[0] == 10  # Первый элемент (по отсортированным ключам)
    assert data.iloc[2] == 300  # Третий элемент
    assert data.iloc[5] == 200  # Шестой элемент
    assert data.iloc[8] == 3  # Последний элемент


def test_minus_keys():
    data = SpecialDict({
        "1": 1,
        "-2": 2,
        "-3": 3
    })
    assert data.iloc[0] == 2
    assert data.iloc[1] == 3


def test_float_keys():
    data = SpecialDict({
        "1.1": 1,
        "2.2": 2,
        "3.3": 3
    })
    assert data.iloc[0] == 1
    assert data.iloc[1] == 2
    assert data.ploc["<2"] == {"1.1": 1}


def test_ploc():
    data = SpecialDict({
        "value1": 1,
        "value2": 2,
        "value3": 3,
        "1": 10,
        "2": 20,
        "3": 30
    })

    assert data.ploc[">=1"] == {"1": 10, "2": 20, "3": 30}
    assert data.ploc["<3"] == {"1": 10, "2": 20}


def test_ploc_key_bracket():
    data = SpecialDict({
        "(1, 5)": 100,
        "(5, 5)": 200,
        "(10, 5)": 300,
        "(1, 5, 3)": 400,
        "(5, 5, 4)": 500,
        "(10, 5, 5)": 600
    })

    assert data.ploc[">0, >0"] == {"(1, 5)": 100, "(5, 5)": 200, "(10, 5)": 300}
    assert data.ploc[">=10, >0"] == {"(10, 5)": 300}
    assert data.ploc["<5, >=5, >=3"] == {"(1, 5, 3)": 400}


def test_parse_error_key():
    data = SpecialDict({",,,,1-1": "test_value"})
    assert data.ploc["<5"] == {}


def test_all_operation():
    data = SpecialDict({
        "(1, 5)": 100,
        "(5, 5)": 200
    })
    assert data.ploc[">10, >10"] == {}
    assert data.ploc[">=10, <5"] == {}
    assert data.ploc["<0, >=5"] == {}
    assert data.ploc["==1, <>5"] == {}
    assert data.ploc["<=0, <=0"] == {}


def test_invalid_condition():
    data = SpecialDict({"1": 10, "2": 20})
    with pytest.raises(InvalidConditionException):
        assert data.ploc["invalid_condition"]
