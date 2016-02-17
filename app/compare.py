import os
import csv

import json

from .driver import Driver

def get_content_from_url(url):
    wms = find_all_wms(url)
    wm_dict = {}

    for wm in wms:
        #extract the text portion of the wm :
        # <TODO some magic>
        class_name = '' # extract the class name from the object
        text = '' # extract the to-be-compared text from the object
        wm_dict[class_name] = text

    return wm_dict


def find_all_wms(url):
    d = Driver()
    res = d.get(url)

   # parse the tree to find all classes whose names start with WMS-.....
    wms = []

   #<TODO some magic>


    return wms


class Structure:

    _expected_dir = None

    def __init__(self, csvfp):
        self.errors = []

        self.csvfp = os.path.abspath(csvfp)
        if not os.path.exists(csvfp):
            raise IOError('File {} does not exist'.format(csvfp))

    @property
    def expected_dir(self):
        if self._expected_dir is None:
            csv_dir = os.path.dirname(os.path.abspath(self.csvfp))
            csvfp_name = os.path.splitext(os.path.basename(self.csvfp))[0]
            self._expected_dir = os.path.join(csv_dir,'expected_{}'.format(csvfp_name))

        return self._expected_dir

    def next_row(self):
        ''' generator which gives the url and name on each call
        '''
        with open(self.csvfp) as f:
            reader = csv.reader(f)
            for row in reader:
                url = row[0].strip()
                name = row[1].strip()
                yield url, name


class Compare(Structure):

    def __init__(self, csvfp):
        super(Compare, self).__init__(csvfp)
        self.run()

    def run(self):
        "read in the given csv and compare the files containing the expected data"


        next_row_data = self.next_row()  # generator which gives the url and row

        for url, name in next_row_data:
                self.compare_expecteds(url, name)


    def compare_expecteds(self, url, name):
        """compare the result of the url call with the file in the subdirectory named "expected... "
        """

        url_content = get_content_from_url(url)
        expected_content = self.get_expected_content(name)
        if url_content != expected_content:
            self.errors.append(url, url_content, expected_content)


    def get_expected_content(self, name):
        fn = os.path.join(self.expected_dir, name)
        with open(fn) as f:
            return f.read()
