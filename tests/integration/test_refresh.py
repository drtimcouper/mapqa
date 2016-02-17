import os

from nose.tools import assert_equal, assert_true, assert_raises
from unittest.mock import patch

import app.refresh as refresh

Refresh = refresh.Refresh

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

class Test_build:

    def test_csv_does_not_exist(self):
        with assert_raises(IOError):
           Refresh('junk')

    def test_duplicate_name(self):
        with patch.object(refresh, 'save_content') as save_content:
            ref = Refresh(os.path.join(DATA_DIR, 'duplicate_name.csv'))
            assert_equal(save_content.call_count,1)
            assert_equal(len(ref.errors), 1)
            assert_equal(ref.errors[0].args, ('python-site',))
