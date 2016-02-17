import os

from nose.tools import assert_equal, assert_raises
from unittest.mock import patch

import app.compare as compare

Compare = compare.Compare

from .fixtures import DATA_DIR


def test_compare_ok():
    # read what's in expected_compare_url  and use this as what comes back
    # from the url call
    fp = os.path.join(DATA_DIR, 'compare-url.csv')
    c = Compare(fp)
    expected_fp = os.path.join(DATA_DIR, 'expected_compare-url', 'compare-me')
    with open(expected_fp) as f:
        url_content = f.read()

    with patch.object(compare, 'get_content_from_url') as get_content:
        get_content.return_value = url_content
        c.run()
    assert_equal(c.errors, [])

def test_compare_fail():
    # read what's in expected_compare_url  and use this as what comes back
    # from the url call
    fp = os.path.join(DATA_DIR, 'compare-url.csv')
    c = Compare(fp)

    with patch.object(compare, 'get_content_from_url') as get_content:
        get_content.return_value = 'something else'
        c.run()
    assert_equal(len(c.errors), 1)


