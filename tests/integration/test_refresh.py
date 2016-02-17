import os
import json

from nose.tools import assert_equal, assert_raises
from unittest.mock import patch

import app.refresh as refresh


Refresh = refresh.Refresh

from .fixtures import DATA_DIR


def test_csv_does_not_exist():
    with assert_raises(IOError):
       Refresh('junk')


def test_ds_duplicate_name():
    with patch.object(refresh, 'get_content_from_url') as get_content:
        with patch.object(Refresh, 'save_content'):
            my_content = {'WMS1': 'my sentinel'}
            get_content.return_value = my_content
            ref = Refresh(os.path.join(DATA_DIR, 'duplicate_name.csv'))
            ref.run()
            assert_equal(get_content.call_count,1)
            assert_equal(len(ref.errors), 1)
            assert_equal(ref.errors[0].args, ('python-site',))


def test_ds_simple():
    with patch.object(refresh, 'get_content_from_url') as get_content:
        my_content = {'WMS1': 'my sentinel'}
        get_content.return_value = my_content
        ref = Refresh(os.path.join(DATA_DIR, 'simple.csv'))
        ref.run()
        files_present = os.listdir(ref.expected_dir)
        assert_equal(len(files_present), 1)

        the_file = os.path.join(ref.expected_dir, files_present[0])
        with open(the_file) as f:
            body = f.read()

        assert_equal(json.loads(body), my_content)
