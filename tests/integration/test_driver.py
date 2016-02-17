from nose.tools import assert_equal, assert_true


import app.driver as driver

Driver = driver.Driver


def test_get_attribute_ok():
    d = Driver()
    assert_equal(d.get, d._driver.get)



