import os

from nose.tools import assert_equal, assert_raises

import app.compare as compare

Structure = compare.Structure

from .fixtures import SIMPLE_CSV, DATA_DIR


def test_constructor():
    with assert_raises(IOError):
        Structure('junk')


def test_expected_dir():
    s = Structure(SIMPLE_CSV)
    exp = os.path.join(DATA_DIR, 'expected_simple')
    assert_equal(exp, s.expected_dir)


def test_expected_dir_cached():
     s = Structure(SIMPLE_CSV)
     exp = os.path.join(DATA_DIR, 'expected_simple')
     assert_equal(exp, s.expected_dir)


def test_next_row():
     s = Structure(SIMPLE_CSV)
     gen = s.next_row()
     res = []
     for url, name in gen:
        res.append((url, name))

     assert_equal(res,[('http://www.python.org', 'python-orig-site')])

