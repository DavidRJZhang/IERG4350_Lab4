import re

def check_name(name):
    return bool(re.match(r'^[\x20-\x7E]+$', name)) and name == name.strip()

def check_name_len(name):
    return len(name.encode('utf-8')) <= 20

def check_sid(sid):
    return bool(re.match(r'^1155\d{6}$', sid))

def test_check_name():
    assert check_name("hello") == True
    assert check_name("he llo") == True
    assert check_name("he1lo") == True
    assert check_name("he1o") == True

def test_check_name_len():
    assert check_name_len("hellohaha") == True
    assert check_name_len("⅞+⅛!=ю") == True
    assert check_name_len("ю ю") == True
    assert check_name_len("⅞+⅛!=ю!!!!") == True

def test_check_sid():
    assert check_sid("1155000000") == True
    assert check_sid("1234567890") == False
    assert check_sid("115500000") == False
    assert check_sid("11550000000") == False

